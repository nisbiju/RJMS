from flask import Blueprint, request, jsonify, session
from ..models.models import db, User, Enrollment, Course
from ..utils.auth_utils import teacher_required

bp = Blueprint('students', __name__, url_prefix='/api/students')

@bp.route('/course/<int:course_id>', methods=['GET'])
@teacher_required
def get_course_students(course_id):
    """Get all students enrolled in a course"""
    course = Course.query.get_or_404(course_id)
    
    if course.teacher_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403
    
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    students = [e.student for e in enrollments]
    
    return jsonify({
        'students': [{
            'id': s.id,
            'name': s.name,
            'email': s.email,
            'profile_image': s.profile_image,
            'enrolled_at': Enrollment.query.filter_by(student_id=s.id, course_id=course_id).first().enrolled_at.isoformat()
        } for s in students]
    }), 200

@bp.route('/course/<int:course_id>', methods=['POST'])
@teacher_required
def add_student_to_course(course_id):
    """Add a student to a course"""
    course = Course.query.get_or_404(course_id)
    
    if course.teacher_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    email = data.get('email')
    name = data.get('name', '')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # Check if student exists
    student = User.query.filter_by(email=email, role='student').first()
    
    if not student:
        # Create new student user if they don't exist
        student = User(
            email=email,
            name=name if name else email.split('@')[0],
            google_id=f'manual_{email}_{course_id}',
            role='student'
        )
        db.session.add(student)
        db.session.flush()  # Get the student ID before enrolling
    
    # Check if already enrolled
    existing = Enrollment.query.filter_by(student_id=student.id, course_id=course_id).first()
    if existing:
        return jsonify({'error': 'Student already enrolled'}), 400
    
    enrollment = Enrollment(student_id=student.id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    
    return jsonify({
        'message': 'Student added successfully',
        'student': {
            'id': student.id,
            'name': student.name,
            'email': student.email
        }
    }), 201

@bp.route('/course/<int:course_id>/bulk', methods=['POST'])
@teacher_required
def bulk_add_students(course_id):
    """Add multiple students from uploaded list"""
    course = Course.query.get_or_404(course_id)
    
    if course.teacher_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    students_data = data.get('students', [])
    
    added = 0
    for student_info in students_data:
        email = student_info.get('email')
        if not email:
            continue
        
        student = User.query.filter_by(email=email, role='student').first()
        if not student:
            # Create new student user
            student = User(
                email=email,
                name=student_info.get('name', email.split('@')[0]),
                google_id=f'manual_{email}',
                role='student'
            )
            db.session.add(student)
            db.session.flush()
        
        # Check if already enrolled
        existing = Enrollment.query.filter_by(student_id=student.id, course_id=course_id).first()
        if not existing:
            enrollment = Enrollment(student_id=student.id, course_id=course_id)
            db.session.add(enrollment)
            added += 1
    
    db.session.commit()
    
    return jsonify({'message': f'{added} students added successfully'}), 201

@bp.route('/<int:student_id>/course/<int:course_id>', methods=['DELETE'])
@teacher_required
def remove_student_from_course(student_id, course_id):
    """Remove a student from a course"""
    course = Course.query.get_or_404(course_id)
    
    if course.teacher_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403
    
    enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first_or_404()
    
    db.session.delete(enrollment)
    db.session.commit()
    
    return jsonify({'message': 'Student removed successfully'}), 200
