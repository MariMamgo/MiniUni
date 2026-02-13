from flask import Blueprint, request, jsonify
from app import db
from models import Enrollment, User, Course
from auth_utils import verify_token
from sqlalchemy.exc import IntegrityError

enrollment_bp = Blueprint('enrollments', __name__, url_prefix='/api/enrollments')

@enrollment_bp.route('', methods=['POST'])
@verify_token
def enroll():
    data = request.get_json()
    
    if not data or not data.get('courseId'):
        return jsonify({'message': 'Course ID required'}), 400
    
    course = Course.query.get(data['courseId'])
    if not course:
        return jsonify({'message': 'Course not found'}), 404
    
    try:
        enrollment = Enrollment(
            studentId=request.user['userId'],
            courseId=data['courseId']
        )
        db.session.add(enrollment)
        db.session.commit()
        
        return jsonify({
            'id': enrollment.id,
            'studentId': enrollment.studentId,
            'courseId': enrollment.courseId,
            'enrollmentDate': enrollment.enrollmentDate.isoformat()
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Already enrolled in this course'}), 400

@enrollment_bp.route('/my-courses', methods=['GET'])
@verify_token
def get_my_courses():
    enrollments = Enrollment.query.filter_by(studentId=request.user['userId']).all()
    
    return jsonify([{
        'id': e.id,
        'courseId': e.courseId,
        'course': {
            'id': e.course.id,
            'name': e.course.name,
            'description': e.course.description,
            'instructor': e.course.instructor
        },
        'enrollmentDate': e.enrollmentDate.isoformat()
    } for e in enrollments]), 200

@enrollment_bp.route('', methods=['GET'])
@verify_token
def get_all_enrollments():
    if request.user['role'] != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    enrollments = Enrollment.query.all()
    
    return jsonify([{
        'id': e.id,
        'studentId': e.studentId,
        'studentEmail': e.student.email,
        'courseId': e.courseId,
        'courseName': e.course.name,
        'enrollmentDate': e.enrollmentDate.isoformat()
    } for e in enrollments]), 200
