# 🎓 Educational Platform - Technology Stack

## Full Stack Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND LAYER                          │
│  React 18 • Vite • Axios • Modern CSS                       │
│  Port: 3000 • Browser: http://localhost:3000                │
└────────────────────────┬────────────────────────────────────┘
                         │ (HTTP/HTTPS)
                         │ REST API Calls
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    API LAYER                                │
│  Flask • SQLAlchemy • JWT Auth • RESTful Design             │
│  Port: 5000 • API: http://localhost:5000/api               │
└────────────────────────┬────────────────────────────────────┘
                         │ (SQL Queries)
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   DATABASE LAYER                            │
│  PostgreSQL • Relational Data • 3 Tables                    │
│  Connection: postgresql://localhost:5432/edu_platform      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Frontend Technologies

### Core
- **React 18.2.0** - UI library & component framework
- **Vite 5.0.0** - Lightning-fast build tool
- **JSX** - React templating language
- **ES6+ JavaScript** - Modern JavaScript features

### HTTP Client
- **Axios 1.6.0** - Promised-based HTTP client
  - Automatic JSON parsing
  - Request/response interceptors
  - Error handling

### Styling
- **CSS3** - Modern styling
  - Grid layouts
  - Flexbox
  - Media queries
  - Animations

### Package Manager
- **npm** (Node Package Manager)
- Node version: 18+ required

### Component Architecture
```
App.jsx (Main)
├── LoginPage.jsx (Auth)
├── StudentDashboard.jsx (Courses)
└── AdminDashboard.jsx (Management)
```

### Build Process
- Development: `npm run dev` → Vite dev server
- Production: `npm run build` → Optimized /dist folder
- Preview: `npm run preview` → Test production build

---

## 🐍 Backend Technologies

### Web Framework
- **Flask 2.3.0** - Lightweight Python web framework
  - Routing & URL handling
  - Request/response handling
  - Blueprint system for modular code

### Database ORM
- **SQLAlchemy 2.0.0** - SQL toolkit & ORM
  - Database abstraction layer
  - Model definition
  - Query building
  - Relationship management

### Database Adapter
- **psycopg2-binary 2.9.6** - PostgreSQL adapter for Python
  - SQL query execution
  - Connection pooling
  - Binary support

### Authentication
- **PyJWT 2.8.0** - JSON Web Token implementation
  - Token generation
  - Token verification
  - Claim validation
  - 30-day expiration

### Security
- **Werkzeug 2.3.0** - WSGI utilities
  - Password hashing (bcrypt-style)
  - Security utilities
  - Data structures

### CORS
- **Flask-CORS 4.0.0** - Cross-Origin Resource Sharing
  - Enables frontend to call backend API
  - Handles preflight requests

### Environment
- **python-dotenv 1.0.0** - Load .env files
  - Configuration management
  - Sensitive data protection

### Server
- **Gunicorn** - WSGI HTTP server (for production)
  - Handles multiple requests
  - Process management

### Package Manager
- **pip** (Python Package Manager)
- Python version: 3.9+ required

### Project Structure
```
backend/
├── app.py (Flask app, routes registration)
├── models.py (User, Course, Enrollment)
└── routes/
    ├── auth_routes.py (Login, Signup)
    ├── course_routes.py (CRUD)
    └── enrollment_routes.py (Enrollment)
```

---

## 💾 Database Technologies

### Database System
- **PostgreSQL 12+** - Advanced open-source RDBMS
  - ACID compliance
  - Complex queries
  - Scalable
  - Free & reliable

### Data Types Used
```sql
INTEGER - User/Course/Enrollment IDs
VARCHAR(120) - Emails, names
TEXT - Descriptions
DateTime - Timestamps
```

### Schema Features
- **Primary Keys** - Unique ID for each record
- **Foreign Keys** - Relationships between tables
- **Unique Constraints** - Prevent duplicate enrollments
- **Timestamps** - Auto-updated on creation

### Tables

**users**
```
id (int, PK)
email (varchar, unique)
password (varchar, hashed)
role (varchar, student|admin)
createdAt (datetime)
```

**courses**
```
id (int, PK)
name (varchar)
description (text)
instructor (varchar)
createdAt (datetime)
```

**enrollments**
```
id (int, PK)
studentId (int, FK → users.id)
courseId (int, FK → courses.id)
enrollmentDate (datetime)
UNIQUE(studentId, courseId)
```

### Relationships
- **One User → Many Enrollments** (1:M)
- **One Course → Many Enrollments** (1:M)
- **Many Students ← Many Courses** (M:M through enrollments)

---

## 🔐 Authentication & Authorization

### Flow
```
1. User enters credentials
2. Backend hashes & verifies password
3. Backend generates JWT token (30-day expiration)
4. Frontend stores token in localStorage
5. Frontend includes token in all API requests
6. Backend verifies token on protected routes
```

### JWT Token Contents
```json
{
  "userId": 123,
  "email": "user@example.com",
  "role": "student",
  "exp": 1700000000
}
```

### Protected Routes
```
POST /api/courses - Admin only
DELETE /api/courses/<id> - Admin only
POST /api/enrollments - Authenticated student
GET /api/enrollments - Admin only
```

---

## 🌐 Communication Protocol

### HTTP Methods Used
- **GET** - Retrieve data
- **POST** - Create data
- **DELETE** - Remove data
- (PUT/PATCH not used currently, but can be added)

### Request/Response Format
```javascript
// Request
POST /api/enrollments
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
{ "courseId": 5 }

// Response (Success)
201 Created
{
  "id": 1,
  "studentId": 3,
  "courseId": 5,
  "enrollmentDate": "2024-02-13T10:30:00"
}

// Response (Error)
400 Bad Request
{
  "message": "Course not found"
}
```

### Status Codes
- 200 - OK (successful GET)
- 201 - Created (successful POST)
- 400 - Bad Request (validation error)
- 401 - Unauthorized (invalid token)
- 403 - Forbidden (insufficient permissions)
- 404 - Not Found (resource missing)
- 500 - Server Error

---

## 📦 Dependency Management

### Frontend Dependencies
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "axios": "^1.6.0"
}
```

### Frontend Dev Dependencies
```json
{
  "@vitejs/plugin-react": "^4.0.0",
  "vite": "^5.0.0"
}
```

### Backend Dependencies (requirements.txt)
```
flask==2.3.0
flask-cors==4.0.0
psycopg2-binary==2.9.6
python-dotenv==1.0.0
pyjwt==2.8.0
werkzeug==2.3.0
sqlalchemy==2.0.0
flask-sqlalchemy==3.0.0
gunicorn==21.0.0  # Production server
```

---

## 🚀 Deployment Stack

### Frontend Deployment
- **Vercel** - Optimized for React/Next.js
- **Features:**
  - Automatic deployments from GitHub
  - CDN with caching
  - Serverless functions (if needed)
  - Environment variables
  - HTTPS automatic

### Backend Deployment
- **Render** - Simple Python deployment
- **Features:**
  - GitHub integration
  - Auto-restart on crash
  - Environment variables
  - HTTPS automatic
  - Free PostgreSQL tier

### Database Deployment
- **Render PostgreSQL** - Managed PostgreSQL
- **Features:**
  - Automatic backups
  - Free 400 MB tier
  - Upgradeable storage
  - Connection pooling
  - Point-in-time recovery

---

## 🎯 Performance Characteristics

### Response Times (Local)
- API Response: 10-50ms
- Database Query: 5-20ms
- Frontend Render: 16ms (60 FPS)

### Scalability
```
Single Server (Render Free):
- ✅ 100-1000 concurrent users
- ✅ 10000+ enrollments
- ✅ 100+ courses

With Upgrades:
- ✅ 10000+ concurrent users
- ✅ 1M+ enrollments
- ✅ 10000+ courses
```

### Database Constraints
- **Free Tier:** 400 MB storage (~50K enrollments)
- **Pro Tier:** 10 GB storage (~5M enrollments)
- **Enterprise:** Unlimited

---

## 🔧 Development vs Production

### Development Configuration
```
Database: PostgreSQL (local)
Frontend: http://localhost:3000
Backend: http://localhost:5000
Debug: Enabled
CORS: Allow all
Environment: development
```

### Production Configuration
```
Database: PostgreSQL (managed on Render)
Frontend: https://yourdomain.vercel.app
Backend: https://api.yourdomain.onrender.com
Debug: Disabled
CORS: Specific domains only
Environment: production
Secret Key: Randomized
```

---

## 📊 Tech Stack Comparison Table

| Aspect | Choice | Why |
|--------|--------|-----|
| Frontend Framework | React | Popular, component-based |
| Frontend Build Tool | Vite | Fast, modern |
| Backend Framework | Flask | Lightweight, Python |
| Database | PostgreSQL | Reliable, scalable, free tier |
| Auth Method | JWT | Stateless, secure |
| Frontend Hosting | Vercel | Best for React |
| Backend Hosting | Render | Best for Python/Flask |
| Database Hosting | Render | Integrated with backend |

---

## 🎓 Why This Stack?

### Best For
- ✅ Learning full-stack development
- ✅ Educational projects
- ✅ Rapid prototyping
- ✅ Free/low-cost deployment
- ✅ Single developer or small team

### Advantages
- ✅ JavaScript on frontend (learner-friendly)
- ✅ Python on backend (readable, educational)
- ✅ All free tier available
- ✅ Easy to deploy
- ✅ Large community & resources
- ✅ Can scale as needed

### Limitations
- ⚠️ Single-server initially (scales with upgrades)
- ⚠️ No real-time features (can add Socket.io)
- ⚠️ No offline support (can add PWA)
- ⚠️ Limited to text/JSON (can add file uploads)

---

## 🔄 Data Flow Example

```
User Enrollment Flow:
1. Student clicks "Enroll Now"
2. Frontend calls: POST /api/enrollments {courseId: 5}
3. Frontend includes JWT token in header
4. Backend receives request
5. Backend verifies JWT token
6. Backend checks if student already enrolled
7. Backend inserts enrollment record
8. Database returns new enrollment ID
9. Backend sends response with 201 Created
10. Frontend receives response
11. Frontend updates UI (button shows "✓ Enrolled")
12. Frontend notifies student "Successfully enrolled!"
```

---

## 📈 Monitoring & Observability

### Logging Points
- Backend: All API requests logged
- Frontend: Console logs for debugging
- Database: Query logs available

### Monitoring Tools
- **Render:** Built-in logs & metrics
- **Vercel:** Deployment logs & performance
- **Browser DevTools:** Network tab for API calls

### Health Checks
- Backend health endpoint: GET /api/health
- Frontend build status: npm run build
- Database connection: Test in Flask startup

---

## 🎓 Learning Resources by Component

### Frontend
- React Tutorial: https://react.dev/learn
- Vite Guide: https://vitejs.dev/guide/
- Axios Documentation: https://axios-http.com/docs
- CSS Guide: https://developer.mozilla.org/en-US/docs/Web/CSS

### Backend
- Flask Tutorial: https://flask.palletsprojects.com/tutorial/
- SQLAlchemy ORM: https://docs.sqlalchemy.org/
- JWT Auth: https://pyjwt.readthedocs.io/
- PostgreSQL: https://www.postgresql.org/docs/

### DevOps
- Vercel Deployment: https://vercel.com/docs
- Render Deployment: https://render.com/docs
- Git Basics: https://git-scm.com/docs

---

## 🎉 You're Ready!

All technologies are properly integrated and documented. Time to build something amazing! 🚀
