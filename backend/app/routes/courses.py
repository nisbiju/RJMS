from flask import Blueprint, request, jsonify, session
from ..models.models import db, Course, Enrollment, User, Reflection
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
    
    # Delete existing reflections to avoid duplicates
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
                    name=f"Reflection {reflection_number}",
                    number=reflection_number,
                    description=f"Reflection journal entry for week {reflection_number}",
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
                name=f"Reflection {reflection_number}",
                number=reflection_number,
                description=f"Reflection journal entry for week {reflection_number}",
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
            'custom_structure': course.custom_structure
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
    
    # Generate reflections based on the configuration
    generate_reflections_for_course(course)
    
    return jsonify({'message': 'Configuration saved successfully'}), 200
