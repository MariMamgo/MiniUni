# Educational Platform

A full-stack web application for managing student course enrollments with admin capabilities. Built with React, Flask, and PostgreSQL.

## Features

- **Student Dashboard**: Browse available courses and enroll
- **Admin Dashboard**: Manage courses (add/remove) and view all student enrollments
- **Authentication**: Secure login system with JWT tokens
- **Database**: PostgreSQL for reliable data storage

## Project Structure

```
website for mini uni/
├── frontend/              # React application
│   ├── src/
│   │   ├── pages/        # Student, Admin, Login pages
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── backend/              # Flask API
│   ├── routes/           # API endpoints
│   ├── models.py         # Database models
│   ├── app.py            # Flask app
│   ├── requirements.txt
│   └── .env
└── README.md
```

## Prerequisites

- Node.js 18+
- Python 3.9+
- PostgreSQL 12+

## Local Development

### 1. Setup Database

```bash
# Create PostgreSQL database
createdb edu_platform
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Update .env with your database credentials
# DATABASE_URL=postgresql://user:password@localhost:5432/edu_platform

# Run Flask server
python app.py
```

Backend will run on `http://localhost:5000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will run on `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user

### Courses
- `GET /api/courses` - List all courses
- `GET /api/courses/<id>` - Get course details
- `POST /api/courses` - Create course (admin only)
- `DELETE /api/courses/<id>` - Delete course (admin only)

### Enrollments
- `POST /api/enrollments` - Enroll in course
- `GET /api/enrollments/my-courses` - Get student's courses
- `GET /api/enrollments` - Get all enrollments (admin only)

## Deployment

### Deploy Backend to Render

1. Push code to GitHub
2. Create new Render account: https://render.com
3. Click "New+" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: edu-platform-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Add Environment Variables:
   - `DATABASE_URL`: (PostgreSQL connection string from Render)
   - `SECRET_KEY`: Generate a strong key
   - `FLASK_ENV`: production

7. Create PostgreSQL database in Render:
   - Click "New+" → "PostgreSQL"
   - Copy connection string to `DATABASE_URL`

### Deploy Frontend to Vercel

1. Push code to GitHub
2. Go to https://vercel.com and sign in with GitHub
3. Click "New Project"
4. Select your repository
5. Configure:
   - **Framework**: Vite
   - **Root Directory**: ./frontend
6. Add Environment Variable:
   - `VITE_API_URL`: `https://your-render-api.onrender.com`
7. Deploy!

## Default Test Accounts

After first run, you can create accounts through signup:
- **Admin Account**: Email: admin@test.com, Password: password123, Role: Admin
- **Student Account**: Email: student@test.com, Password: password123, Role: Student

## Security Notes

- Change `SECRET_KEY` in production
- Use HTTPS for all connections
- Store environment variables securely
- Implement rate limiting for production

## Troubleshooting

### Connection refused error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env

### CORS errors
- Backend CORS is enabled for development
- For production, update CORS settings in `app.py`

### Frontend can't connect to API
- Ensure backend is running on port 5000
- Check proxy settings in `vite.config.js`

## Next Steps

- Add email verification
- Implement course materials/content
- Add student grades and progress tracking
- Create course schedules
- Add notifications system

## License

MIT
# MiniUni
