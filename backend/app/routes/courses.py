from flask import Blueprint, request, jsonify, session
from ..models.models import db, Course, Enrollment, User, Reflection, ReflectionSubmission
from ..utils.auth_utils import login_required, teacher_required
from datetime import datetime, timedelta

bp = Blueprint('courses', __name__, url_prefix='/api/courses')

def generate_reflections_for_course(course):
    """Generate reflection instances based on course configuration"""
    print(f"\n[DEBUG] generate_reflections_for_course called for course {course.id}")
    print(f"[DEBUG] Start date: {course.start_date}, End date: {course.end_date}")
    
    if not course.start_date or not course.end_date:
        print(f"[DEBUG] Missing dates - Start: {course.start_date}, End: {course.end_date}")
        return
    
    # Check if any reflections in this course have submissions
    existing_reflections = Reflection.query.filter_by(course_id=course.id).all()
    has_submissions = False
    
    for reflection in existing_reflections:
        submission_count = ReflectionSubmission.query.filter_by(reflection_id=reflection.id).count()
        if submission_count > 0:
            has_submissions = True
            break
    
    if has_submissions:
        print(f"[DEBUG] Course has existing submissions - skipping reflection regeneration")
        print(f"[DEBUG] Updating structure for existing reflections instead")
        # Update structure for existing reflections
        structure = course.custom_structure if course.custom_structure else None
        for reflection in existing_reflections:
            reflection.structure = structure
        db.session.commit()
        return
    
    # Delete existing reflections to avoid duplicates (only if no submissions)
    deleted_count = Reflection.query.filter_by(course_id=course.id).delete()
    print(f"[DEBUG] Deleted {deleted_count} existing reflections")
    
    # Get reflection structure from course
    structure = course.custom_structure if course.custom_structure else None
    
    # Generate reflections based on recurrence pattern
    reflections_to_create = []
    current_date = course.start_date
    reflection_number = 1
    
    # Map day names to weekday numbers (Monday=0, Sunday=6)
    # Support both full names and abbreviations
    day_map = {
        'Monday': 0, 'Mon': 0,
        'Tuesday': 1, 'Tues': 1, 'Tue': 1,
        'Wednesday': 2, 'Wed': 2,
        'Thursday': 3, 'Thurs': 3, 'Thu': 3,
        'Friday': 4, 'Fri': 4,
        'Saturday': 5, 'Sat': 5,
        'Sunday': 6, 'Sun': 6
    }
    
    # Parse selected days if provided
    selected_weekdays = None
    if course.selected_days:
        selected_day_names = [d.strip() for d in course.selected_days.split(',')]
        selected_weekdays = [day_map[day] for day in selected_day_names if day in day_map]
        print(f"[DEBUG] Selected days: {course.selected_days} -> weekdays: {selected_weekdays}")
    
    if selected_weekdays is not None:
        # When specific days are selected, iterate day by day
        while current_date <= course.end_date:
            # Check if current day is one of the selected weekdays
            if current_date.weekday() in selected_weekdays:
                # Calculate due date
                due_days = course.reflection_due_days if course.reflection_due_days else 7
                due_date = current_date + timedelta(days=due_days)
                
                # Create reflection
                reflection = Reflection(
                    course_id=course.id,
                    name=f"Reflection {current_date.strftime('%d/%m')}",
                    number=reflection_number,
                    description=f"",
                    start_date=current_date,
                    due_date=due_date,
                    structure=structure
                )
                reflections_to_create.append(reflection)
                reflection_number += 1
            
            # Move to next day
            current_date += timedelta(days=1)
    else:
        # When no specific days selected, use recurrence_days
        while current_date <= course.end_date:
            # Calculate due date
            due_days = course.reflection_due_days if course.reflection_due_days else 7
            due_date = current_date + timedelta(days=due_days)
            
            # Create reflection
            reflection = Reflection(
                course_id=course.id,
                name=f"Reflection {current_date.strftime('%d/%m')}",
                number=reflection_number,
                description=f"",
                start_date=current_date,
                due_date=due_date,
                structure=structure
            )
            reflections_to_create.append(reflection)
            reflection_number += 1
            
            # Move to next occurrence based on recurrence_days
            recurrence = course.recurrence_days if course.recurrence_days else 7
            current_date += timedelta(days=recurrence)
    
    # Bulk insert reflections
    print(f"[DEBUG] Total reflections to create: {len(reflections_to_create)}")
    if reflections_to_create:
        db.session.bulk_save_objects(reflections_to_create)
        db.session.commit()
        print(f"[DEBUG] Successfully created {len(reflections_to_create)} reflections")
    else:
        print("[DEBUG] No reflections created")

@bp.route('', methods=['GET'])
@login_required
def get_courses():
    """Get courses based on user role"""
    user = User.query.get(session['user_id'])
    
    if user.role == 'teacher':
        courses = Course.query.filter_by(teacher_id=user.id).all()
    else:
        # Get enrolled courses for students
        enrollments = Enrollment.query.filter_by(student_id=user.id).all()
        courses = [e.course for e in enrollments]
    
    search = request.args.get('search', '').lower()
    status_filter = request.args.get('status')
    
    # Filter courses
    filtered_courses = courses
    if search:
        filtered_courses = [c for c in filtered_courses if search in c.name.lower() or (c.course_code and search in c.course_code.lower())]
    
    if status_filter and status_filter != 'all':
        filtered_courses = [c for c in filtered_courses if c.status == status_filter]
    
    return jsonify({
        'courses': [{
            'id': c.id,
            'name': c.name,
            'course_code': c.course_code,
            'status': c.status,
            'teacher_id': c.teacher_id,
            'start_date': c.start_date.isoformat() if c.start_date else None,
            'end_date': c.end_date.isoformat() if c.end_date else None,
            'framework': c.framework
        } for c in filtered_courses]
    }), 200

@bp.route('/<int:course_id>', methods=['GET'])
@login_required
def get_course(course_id):
    """Get specific course details"""
    course = Course.query.get_or_404(course_id)
    user = User.query.get(session['user_id'])
    
    # Check access
    if user.role == 'teacher' and course.teacher_id != user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    if user.role == 'student':
        enrollment = Enrollment.query.filter_by(student_id=user.id, course_id=course_id).first()
        if not enrollment:
            return jsonify({'error': 'Not enrolled in this course'}), 403
    
    # Get existing reflections for this course
    reflections = Reflection.query.filter_by(course_id=course_id).order_by(Reflection.start_date).all()
    existing_reflection_dates = [r.start_date.isoformat() if r.start_date else None for r in reflections]
    
    return jsonify({
        'course': {
            'id': course.id,
            'name': course.name,
            'course_code': course.course_code,
            'status': course.status,
            'teacher_id': course.teacher_id,
            'framework': course.framework,
            'start_date': course.start_date.isoformat() if course.start_date else None,
            'end_date': course.end_date.isoformat() if course.end_date else None,
            'reflection_due_days': course.reflection_due_days,
            'recurrence_days': course.recurrence_days,
            'selected_days': course.selected_days,
            'custom_structure': course.custom_structure,
            'existing_reflection_dates': existing_reflection_dates
        }
    }), 200

@bp.route('', methods=['POST'])
@teacher_required
def create_course():
    """Create a new course"""
    data = request.get_json()
    user_id = session['user_id']
    
    course = Course(
        name=data['name'],
        course_code=data.get('course_code'),
        teacher_id=user_id,
        status='active'
    )
    
    db.session.add(course)
    db.session.commit()
    
    return jsonify({
        'course': {
            'id': course.id,
            'name': course.name,
            'course_code': course.course_code,
            'status': course.status
        }
    }), 201

@bp.route('/<int:course_id>/configure', methods=['PUT'])
@teacher_required
def configure_course(course_id):
    """Configure course settings"""
    course = Course.query.get_or_404(course_id)
    
    if course.teacher_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    
    if 'framework' in data:
        course.framework = data['framework']
    if 'start_date' in data:
        course.start_date = datetime.fromisoformat(data['start_date'].replace('Z', ''))
    if 'end_date' in data:
        course.end_date = datetime.fromisoformat(data['end_date'].replace('Z', ''))
    if 'reflection_due_days' in data:
        course.reflection_due_days = data['reflection_due_days']
    if 'recurrence_days' in data:
        course.recurrence_days = data['recurrence_days']
    if 'selected_days' in data:
        course.selected_days = ','.join(data['selected_days']) if isinstance(data['selected_days'], list) else data['selected_days']
    if 'custom_structure' in data:
        course.custom_structure = data['custom_structure']
    
    db.session.commit()
    
    # Handle reflection dates
    if 'selected_reflection_dates' in data and data['selected_reflection_dates']:
        # User has explicitly selected which dates to keep
        manage_reflections_by_dates(course, data['selected_reflection_dates'])
    else:
        # Generate reflections based on the configuration (legacy behavior)
        generate_reflections_for_course(course)
    
    return jsonify({'message': 'Configuration saved successfully'}), 200

def manage_reflections_by_dates(course, selected_dates):
    """Manage reflections based on explicitly selected dates"""
    print(f"\n[DEBUG] manage_reflections_by_dates called for course {course.id}")
    print(f"[DEBUG] Selected dates: {selected_dates}")
    
    # Convert selected dates to datetime objects
    selected_date_objs = []
    for date_str in selected_dates:
        try:
            # Parse ISO date string and convert to datetime at midnight
            parsed = datetime.fromisoformat(date_str.replace('Z', ''))
            # If it's already a date object, convert to datetime
            if isinstance(parsed, datetime):
                date_obj = parsed
            else:
                # It's a date object, convert to datetime
                from datetime import date as date_class
                date_obj = datetime.combine(parsed, datetime.min.time())
            selected_date_objs.append(date_obj)
        except Exception as e:
            print(f"[DEBUG] Failed to parse date: {date_str}, error: {e}")
            continue
    
    # Get existing reflections
    existing_reflections = Reflection.query.filter_by(course_id=course.id).all()
    existing_reflection_map = {r.start_date.date() if r.start_date else None: r for r in existing_reflections}
    
    # Get reflection structure
    structure = course.custom_structure if course.custom_structure else None
    
    # Track which dates we've processed
    processed_dates = set()
    
    # Update or create reflections for selected dates
    reflection_number = 1
    for date_obj in sorted(selected_date_objs):
        date_only = date_obj.date()
        processed_dates.add(date_only)
        
        if date_only in existing_reflection_map:
            # Update existing reflection
            reflection = existing_reflection_map[date_only]
            reflection.structure = structure
            print(f"[DEBUG] Updated existing reflection for {date_only}")
        else:
            # Create new reflection
            due_days = course.reflection_due_days if course.reflection_due_days else 7
            due_date = date_obj + timedelta(days=due_days)
            
            reflection = Reflection(
                course_id=course.id,
                name=f"Reflection {date_obj.strftime('%d/%m')}",
                number=reflection_number,
                description="",
                start_date=date_obj,
                due_date=due_date,
                structure=structure
            )
            db.session.add(reflection)
            print(f"[DEBUG] Created new reflection for {date_only}")
        
        reflection_number += 1
    
    # Delete reflections not in selected dates (only if they have no submissions)
    for date_only, reflection in existing_reflection_map.items():
        if date_only not in processed_dates:
            # Check if this reflection has submissions
            submission_count = ReflectionSubmission.query.filter_by(reflection_id=reflection.id).count()
            if submission_count == 0:
                db.session.delete(reflection)
                print(f"[DEBUG] Deleted reflection for {date_only} (no submissions)")
            else:
                print(f"[DEBUG] Kept reflection for {date_only} (has {submission_count} submissions)")
    
    db.session.commit()
    print(f"[DEBUG] Reflection management complete")
