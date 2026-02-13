# Project Structure Overview

```
website for mini uni/
│
├── frontend/                    # React application
│   ├── src/
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx               # Auth page (login/signup)
│   │   │   ├── LoginPage.css
│   │   │   ├── StudentDashboard.jsx        # Student course listing & enrollment
│   │   │   ├── StudentDashboard.css
│   │   │   ├── AdminDashboard.jsx          # Admin panel (manage courses & view enrollments)
│   │   │   └── AdminDashboard.css
│   │   ├── App.jsx                          # Main app component with routing
│   │   ├── App.css
│   │   ├── main.jsx                         # Entry point
│   │   └── index.css                        # Global styles
│   ├── index.html                          # HTML template
│   ├── package.json                        # NPM dependencies
│   ├── vite.config.js                      # Vite configuration
│   ├── .env.example                        # Environment variables template
│   └── .gitignore
│
├── backend/                     # Flask API
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py                  # User signup/login endpoints
│   │   ├── course_routes.py                # Course CRUD endpoints
│   │   └── enrollment_routes.py            # Enrollment endpoints
│   ├── models.py                           # Database models (User, Course, Enrollment)
│   ├── app.py                              # Flask app initialization
│   ├── requirements.txt                    # Python dependencies
│   ├── .env                                # Environment variables (don't commit)
│   ├── .env.example                        # Environment template
│   └── venv/                               # Python virtual environment (excluded from git)
│
├── README.md                   # Main documentation
├── QUICKSTART.md               # Quick start guide
├── DEPLOYMENT.md               # Deployment instructions
├── setup.sh                    # Setup script
├── .gitignore                  # Git ignore rules
└── This file                   # Folder structure explanation
```

## Component Details

### Frontend Components

**LoginPage.jsx**
- Handles user registration and login
- Stores JWT token in localStorage
- Routes to appropriate dashboard based on role

**StudentDashboard.jsx**
- Fetches all available courses
- Shows enrolled courses
- Allows enrollment via "Enroll Now" button

**AdminDashboard.jsx**
- Add new courses form
- List all courses with enrollment count
- View all student enrollments in table format
- Delete courses functionality

### Backend Structure

**models.py**
```python
- User: Stores student/admin accounts
- Course: Stores course information
- Enrollment: Links students to courses (M2M relationship)
```

**auth_routes.py**
- `/signup` - Register new user
- `/login` - Authenticate user, return JWT token
- `verify_token()` - Decorator to check auth

**course_routes.py**
- `GET /courses` - List all courses
- `POST /courses` - Create course (admin only)
- `DELETE /courses/<id>` - Delete course (admin only)

**enrollment_routes.py**
- `POST /enrollments` - Enroll student in course
- `GET /enrollments/my-courses` - Get student's enrolled courses
- `GET /enrollments` - Get all enrollments (admin only)

## Database Schema

### Users Table
```sql
id | email | password | role | createdAt
```

### Courses Table
```sql
id | name | description | instructor | createdAt
```

### Enrollments Table
```sql
id | studentId | courseId | enrollmentDate
(Unique constraint: studentId + courseId)
```

## Key Technologies

**Frontend:**
- React 18 - UI framework
- Vite - Build tool
- Axios - HTTP requests
- CSS3 - Styling

**Backend:**
- Flask - Python web framework
- SQLAlchemy - ORM
- PostgreSQL - Database
- JWT - Authentication

## File Size Reference

- Frontend source: ~15 KB
- Backend source: ~8 KB
- Total setup size: ~50 MB (includes dependencies)

## Common File Modifications

When deploying, you'll typically update:
1. `backend/.env` - Database credentials, SECRET_KEY
2. `frontend/.env` - API endpoint URL
3. `backend/app.py` - CORS settings for production domain

## Running Commands

```bash
# Backend
cd backend && source venv/bin/activate && python app.py

# Frontend
cd frontend && npm run dev

# Building for production
# Backend: Ready to deploy as-is
# Frontend: npm run build (creates /dist folder)
```

## Environment Variables

**Backend (.env)**
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT signing key
- `FLASK_ENV` - development/production
- `PORT` - Server port

**Frontend (.env)**
- `VITE_API_URL` - Backend API URL

---

See QUICKSTART.md for setup instructions!
