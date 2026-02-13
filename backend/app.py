from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from functools import wraps

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    # Render uses postgres:// which is deprecated, convert to postgresql://
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or os.getenv(
    'DATABASE_URL',
    'postgresql://user:password@localhost:5432/edu_platform'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student')
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructor = db.Column(db.String(120), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade='all, delete-orphan')

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    courseId = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrollmentDate = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('studentId', 'courseId', name='unique_enrollment'),)

# Auth decorator
def verify_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token required'}), 401
        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user = data
        except:
            return jsonify({'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

# Auth Routes
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password required'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    hashed_password = generate_password_hash(data['password'])
    role = data.get('role', 'student')
    new_user = User(email=data['email'], password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()
    token = jwt.encode({
        'userId': new_user.id,
        'email': new_user.email,
        'role': new_user.role,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, SECRET_KEY, algorithm='HS256')
    return jsonify({
        'token': token,
        'userId': new_user.id,
        'role': new_user.role,
        'email': new_user.email
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password required'}), 400
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401
    token = jwt.encode({
        'userId': user.id,
        'email': user.email,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, SECRET_KEY, algorithm='HS256')
    return jsonify({
        'token': token,
        'userId': user.id,
        'role': user.role,
        'email': user.email
    }), 200

# Course Routes
@app.route('/api/courses', methods=['GET'])
def get_all_courses():
    courses = Course.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'instructor': c.instructor,
        'createdAt': c.createdAt.isoformat()
    } for c in courses]), 200

@app.route('/api/courses/<int:course_id>', methods=['GET'])
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

@app.route('/api/courses', methods=['POST'])
@verify_token
def create_course():
    if request.user['role'] != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    data = request.get_json()
    if not data or not data.get('name') or not data.get('description') or not data.get('instructor'):
        return jsonify({'message': 'Name, description, and instructor required'}), 400
    new_course = Course(name=data['name'], description=data['description'], instructor=data['instructor'])
    db.session.add(new_course)
    db.session.commit()
    return jsonify({
        'id': new_course.id,
        'name': new_course.name,
        'description': new_course.description,
        'instructor': new_course.instructor
    }), 201

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
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

# Enrollment Routes
@app.route('/api/enrollments', methods=['POST'])
@verify_token
def enroll():
    data = request.get_json()
    if not data or not data.get('courseId'):
        return jsonify({'message': 'Course ID required'}), 400
    course = Course.query.get(data['courseId'])
    if not course:
        return jsonify({'message': 'Course not found'}), 404
    try:
        enrollment = Enrollment(studentId=request.user['userId'], courseId=data['courseId'])
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

@app.route('/api/enrollments/my-courses', methods=['GET'])
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

@app.route('/api/enrollments', methods=['GET'])
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

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

def init_database():
    """Initialize database with default courses and admin account"""
    with app.app_context():
        db.create_all()
        
        # Check if courses exist
        if Course.query.count() > 0:
            return
        
        # Add Georgian courses
        courses_data = [
            {
                'name': 'კალკულუსი',
                'description': 'გამოთვლების საფუძველი - ლიმიტები, წარმოებულები, ინტეგრალები',
                'instructor': 'ა.გ. მათემატიკა'
            },
            {
                'name': 'წრფივი ალგებრა',
                'description': 'ვექტორები, მატრიცები, სიმეტრიული სისტემები',
                'instructor': 'ბ.კ. ალგებრა'
            },
            {
                'name': 'დისკრეტული სტრუქტურები',
                'description': 'სიმრავლეები, გრაფები, ლოგიკა, მთელი რიცხვები',
                'instructor': 'გ.მ. დისკრეტული მათემატიკა'
            },
            {
                'name': 'პითონის საწყისები',
                'description': 'პითონის ენის საფუძვლები, ფუნქციები, მოდულები',
                'instructor': 'დ.ს. პროგრამირება'
            },
            {
                'name': 'ჯავას საწყისები',
                'description': 'ობიექტ-ორიენტირებული პროგრამირება, კლასები, მიმოწერა',
                'instructor': 'ე.ი. ჯავა'
            }
        ]
        
        for course_data in courses_data:
            course = Course(
                name=course_data['name'],
                description=course_data['description'],
                instructor=course_data['instructor']
            )
            db.session.add(course)
        
        # Create admin user if doesn't exist
        admin = User.query.filter_by(email='admin@uni.ge').first()
        if not admin:
            admin = User(
                email='admin@uni.ge',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
        
        db.session.commit()

if __name__ == '__main__':
    init_database()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
