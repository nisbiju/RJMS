from flask import Blueprint, jsonify, session
from ..models.models import Course, Reflection, ReflectionSubmission, Enrollment
from ..utils.auth_utils import teacher_required

bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')

@bp.route('/course/<int:course_id>/overview', methods=['GET'])
@teacher_required
def get_course_overview(course_id):
    """Get course overview statistics"""
    course = Course.query.get_or_404(course_id)
    
    if course.teacher_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403
    
    reflections = Reflection.query.filter_by(course_id=course_id).all()
    total_students = Enrollment.query.filter_by(course_id=course_id).count()
    
    overview_data = []
    for reflection in reflections:
        submissions_count = ReflectionSubmission.query.filter_by(
            reflection_id=reflection.id
        ).filter(ReflectionSubmission.submitted_at.isnot(None)).count()
        
        overview_data.append({
            'reflection_name': reflection.name,
            'reflections_received': submissions_count,
            'total_enrolled_students': total_students
        })
    
    return jsonify({
        'overview': overview_data,
        'total_students': total_students,
        'total_reflections': len(reflections)
    }), 200
