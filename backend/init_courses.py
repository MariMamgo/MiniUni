#!/usr/bin/env python3
"""Initialize courses in the database"""

import os
import sys
from dotenv import load_dotenv
from app import app, db, Course, User
from werkzeug.security import generate_password_hash

load_dotenv()

# Georgian courses
COURSES = [
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

def init_db():
    """Initialize the database with courses"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Delete existing courses
        existing_count = Course.query.count()
        if existing_count > 0:
            print(f"Deleting {existing_count} existing courses...")
            Course.query.delete()
            db.session.commit()
        
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
            print("Created admin user: admin@uni.ge")
        
        # Add courses
        for course_data in COURSES:
            course = Course(
                name=course_data['name'],
                description=course_data['description'],
                instructor=course_data['instructor']
            )
            db.session.add(course)
        
        db.session.commit()
        print(f"\nSuccessfully added {len(COURSES)} Georgian courses:")
        for course in COURSES:
            print(f"  ✓ {course['name']}")

if __name__ == '__main__':
    init_db()
