from flask import Blueprint, request, jsonify, session
from ..models.models import db, Reflection, ReflectionSubmission, Course, Enrollment, User
from ..utils.auth_utils import login_required, teacher_required, student_required
from ..services.ai_feedback import generate_reflection_feedback
from datetime import datetime

bp = Blueprint('reflections', __name__, url_prefix='/api/reflections')

@bp.route('/course/<int:course_id>', methods=['GET'])
@login_required
def get_course_reflections(course_id):
    """Get all reflections for a course"""
    reflections = Reflection.query.filter_by(course_id=course_id).order_by(Reflection.number).all()
    user = User.query.get(session['user_id'])
    
    result = []
    for r in reflections:
        reflection_data = {
            'id': r.id,
            'name': r.name,
            'number': r.number,
            'description': r.description,
            'start_date': r.start_date.isoformat() if r.start_date else None,
            'due_date': r.due_date.isoformat() if r.due_date else None,
            'structure': r.structure
        }
        
        if user.role == 'student':
            submission = ReflectionSubmission.query.filter_by(
                reflection_id=r.id,
                student_id=user.id
            ).first()
            
            reflection_data['submission'] = {
                'id': submission.id,
                'submitted': submission.submitted_at is not None,
                'submitted_at': submission.submitted_at.isoformat() if submission.submitted_at else None,
                'feedback': submission.ai_feedback if submission.display_feedback else None
            } if submission else None
        
        result.append(reflection_data)
    
    return jsonify({'reflections': result}), 200

@bp.route('/<int:reflection_id>', methods=['GET'])
@login_required
def get_reflection(reflection_id):
    """Get specific reflection details"""
    reflection = Reflection.query.get_or_404(reflection_id)
    user = User.query.get(session['user_id'])
    
    data = {
        'id': reflection.id,
        'name': reflection.name,
        'number': reflection.number,
        'description': reflection.description,
        'start_date': reflection.start_date.isoformat() if reflection.start_date else None,
        'due_date': reflection.due_date.isoformat() if reflection.due_date else None,
        'structure': reflection.structure,
        'course_id': reflection.course_id
    }
    
    if user.role == 'student':
        submission = ReflectionSubmission.query.filter_by(
            reflection_id=reflection_id,
            student_id=user.id
        ).first()
        
        if not submission:
            submission = ReflectionSubmission(
                reflection_id=reflection_id,
                student_id=user.id
            )
            db.session.add(submission)
            db.session.commit()
        
        data['submission'] = {
            'id': submission.id,
            'content': submission.content,
            'submitted': submission.submitted_at is not None,
            'submitted_at': submission.submitted_at.isoformat() if submission.submitted_at else None,
            'feedback': submission.ai_feedback if submission.display_feedback else None
        }
    
    return jsonify(data), 200

@bp.route('/submit', methods=['POST'])
@student_required
def submit_reflection():
    """Submit a reflection"""
    data = request.get_json()
    reflection_id = data.get('reflection_id')
    content = data.get('content')
    
    # Get the reflection to check due date
    reflection = Reflection.query.get_or_404(reflection_id)
    
    # Check if due date has passed
    if reflection.due_date and reflection.due_date < datetime.utcnow():
        return jsonify({'error': 'Submission deadline has passed'}), 403
    
    submission = ReflectionSubmission.query.filter_by(
        reflection_id=reflection_id,
        student_id=session['user_id']
    ).first()
    
    if not submission:
        submission = ReflectionSubmission(
            reflection_id=reflection_id,
            student_id=session['user_id']
        )
        db.session.add(submission)
    
    submission.content = content
    submission.submitted_at = datetime.utcnow()
    
    # Get course details for AI feedback context
    course = Course.query.get(reflection.course_id)
    
    # Generate AI-powered feedback using Gemini
    try:
        submission.ai_feedback = generate_reflection_feedback(
            reflection_content=content,
            framework=course.framework if course else None,
            structure=reflection.structure
        )
        print(f"[AI] Generated feedback for reflection {reflection_id}")
    except Exception as e:
        print(f"[AI] Error generating feedback: {str(e)}")
        # Fallback to generic feedback if AI fails
        submission.ai_feedback = "Thank you for your thoughtful reflection. Keep up the great work!"
    
    db.session.commit()
    
    return jsonify({'message': 'Reflection submitted successfully'}), 200

@bp.route('/<int:reflection_id>/submissions', methods=['GET'])
@teacher_required
def get_reflection_submissions(reflection_id):
    """Get all submissions for a reflection (teacher view)"""
    reflection = Reflection.query.get_or_404(reflection_id)
    course = Course.query.get(reflection.course_id)
    
    if course.teacher_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403
    
    enrollments = Enrollment.query.filter_by(course_id=course.id).all()
    
    submissions_data = []
    for enrollment in enrollments:
        student = enrollment.student
        submission = ReflectionSubmission.query.filter_by(
            reflection_id=reflection_id,
            student_id=student.id
        ).first()
        
        submissions_data.append({
            'student_id': student.id,
            'student_name': student.name,
            'student_email': student.email,
            'submitted': submission.submitted_at is not None if submission else False,
            'submission_date': submission.submitted_at.isoformat() if submission and submission.submitted_at else None,
            'content': submission.content if submission else None,
            'ai_feedback': submission.ai_feedback if submission else None,
            'score': submission.score if submission else None,
            'display_feedback': submission.display_feedback if submission else False,
            'submission_id': submission.id if submission else None
        })
    
    return jsonify({'submissions': submissions_data}), 200

@bp.route('/submission/<int:submission_id>/update', methods=['PUT'])
@teacher_required
def update_submission(submission_id):
    """Update submission score, feedback display, and AI feedback"""
    submission = ReflectionSubmission.query.get_or_404(submission_id)
    reflection = Reflection.query.get(submission.reflection_id)
    course = Course.query.get(reflection.course_id)
    
    if course.teacher_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    
    if 'score' in data:
        submission.score = data['score']
    if 'display_feedback' in data:
        submission.display_feedback = data['display_feedback']
    if 'ai_feedback' in data:
        submission.ai_feedback = data['ai_feedback']
    
    db.session.commit()
    
    return jsonify({'message': 'Submission updated successfully'}), 200

@bp.route('/dashboard', methods=['GET'])
@student_required
def get_student_dashboard():
    """Get student dashboard with due/overdue reflections"""
    user_id = session['user_id']
    sort_by = request.args.get('sort_by', 'dates')  # 'dates' or 'courses'
    
    enrollments = Enrollment.query.filter_by(student_id=user_id).all()
    course_ids = [e.course_id for e in enrollments]
    
    reflections = Reflection.query.filter(Reflection.course_id.in_(course_ids)).all()
    
    dashboard_data = []
    now = datetime.utcnow()
    
    for reflection in reflections:
        if reflection.due_date and reflection.due_date >= now:
            submission = ReflectionSubmission.query.filter_by(
                reflection_id=reflection.id,
                student_id=user_id
            ).first()
            
            is_submitted = submission and submission.submitted_at is not None
            
            if not is_submitted or (reflection.due_date and reflection.due_date < now):
                course = Course.query.get(reflection.course_id)
                dashboard_data.append({
                    'reflection_id': reflection.id,
                    'reflection_name': reflection.name,
                    'course_name': course.name,
                    'course_code': course.course_code,
                    'due_date': reflection.due_date.isoformat() if reflection.due_date else None,
                    'is_overdue': reflection.due_date < now if reflection.due_date else False
                })
    
    # Sort
    if sort_by == 'dates':
        dashboard_data.sort(key=lambda x: x['due_date'] if x['due_date'] else '')
    else:  # sort by courses
        dashboard_data.sort(key=lambda x: (x['course_name'], x['reflection_name']))
    
    return jsonify({'reflections': dashboard_data}), 200
