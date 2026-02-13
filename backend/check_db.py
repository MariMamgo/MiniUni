from app import app, db, User, Course, Enrollment

with app.app_context():
    print("=" * 60)
    print("📋 USERS")
    print("=" * 60)
    users = User.query.all()
    for u in users:
        print(f"ID: {u.id} | Email: {u.email} | Role: {u.role} | Created: {u.createdAt}")
    
    print("\n" + "=" * 60)
    print("📚 COURSES")
    print("=" * 60)
    courses = Course.query.all()
    for c in courses:
        print(f"ID: {c.id} | {c.name} | Instructor: {c.instructor}")
    
    print("\n" + "=" * 60)
    print("🎓 ENROLLMENTS")
    print("=" * 60)
    enrollments = Enrollment.query.all()
    if enrollments:
        for e in enrollments:
            print(f"Student: {e.student.email} | Course: {e.course.name} | Date: {e.enrollmentDate}")
    else:
        print("No enrollments yet")
    
    print("\n" + "=" * 60)
    print(f"Total: {len(users)} users | {len(courses)} courses | {len(enrollments)} enrollments")
    print("=" * 60)
