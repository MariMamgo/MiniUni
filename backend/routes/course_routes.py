from flask import Blueprint, request, jsonify
from app import db
from models import Course
from auth_utils import verify_token

course_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

@course_bp.route('', methods=['GET'])
def get_all_courses():
    courses = Course.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'instructor': c.instructor,
        'createdAt': c.createdAt.isoformat()
    } for c in courses]), 200

@course_bp.route('/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Course not found'}), 404
    
    return jsonify({
        'id': course.id,
        'name': course.name,
        'description': course.description,
        'instructor': course.instructor,
        'createdAt': course.createdAt.isoformat()
    }), 200

@course_bp.route('', methods=['POST'])
@verify_token
def create_course():
    if request.user['role'] != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('description') or not data.get('instructor'):
        return jsonify({'message': 'Name, description, and instructor required'}), 400
    
    new_course = Course(
        name=data['name'],
        description=data['description'],
        instructor=data['instructor']
    )
    
    db.session.add(new_course)
    db.session.commit()
    
    return jsonify({
        'id': new_course.id,
        'name': new_course.name,
        'description': new_course.description,
        'instructor': new_course.instructor
    }), 201

@course_bp.route('/<int:course_id>', methods=['DELETE'])
@verify_token
def delete_course(course_id):
    if request.user['role'] != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Course not found'}), 404
    
    db.session.delete(course)
    db.session.commit()
    
    return jsonify({'message': 'Course deleted'}), 200
