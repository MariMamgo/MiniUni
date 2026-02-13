"""
WSGI entry point for production (Render, Heroku, etc.)
Initializes the database before starting the app
"""
from app import app, db, User, Course
from werkzeug.security import generate_password_hash

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
        print("Database initialized successfully!")

# Initialize database on startup
init_database()
