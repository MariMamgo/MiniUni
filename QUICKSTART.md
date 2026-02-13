# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Node.js 18+ (from https://nodejs.org)
- Python 3.9+ (from https://www.python.org)
- PostgreSQL (from https://www.postgresql.org/download)

### macOS Setup

```bash
# 1. Create database
createdb edu_platform

# 2. Set up backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Update .env with your database credentials
# Then start backend:
python app.py

# 3. In a NEW terminal, set up frontend
cd frontend
npm install
npm run dev
```

✅ Open http://localhost:3000

---

### Windows Setup

```bash
# 1. Create database
# Use pgAdmin or psql:
createdb edu_platform

# 2. Set up backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Update .env with your database credentials
# Then start backend:
python app.py

# 3. In a NEW terminal, set up frontend
cd frontend
npm install
npm run dev
```

✅ Open http://localhost:3000

---

### Linux Setup

```bash
# 1. Create database
createdb edu_platform

# 2. Set up backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Update .env with your database credentials
# Then start backend:
python3 app.py

# 3. In a NEW terminal, set up frontend
cd frontend
npm install
npm run dev
```

✅ Open http://localhost:3000

---

## 📋 Database Setup Help

### Installing PostgreSQL

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Windows:**
- Download from https://www.postgresql.org/download/windows/
- Run installer
- Remember the password you set!

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
```

### Creating Database

```bash
# Using psql
psql -U postgres
# Enter password when prompted

# In psql console, run:
CREATE DATABASE edu_platform;
\q

# Exit with Ctrl+D
```

---

## 🔒 Default Test Logins

After first run, create accounts:

**Admin Account:**
- Email: admin@test.com
- Password: password123
- Role: Admin

**Student Account 1:**
- Email: student1@test.com
- Password: password123
- Role: Student

**Student Account 2:**
- Email: student2@test.com
- Password: password123
- Role: Student

---

## 🐛 Troubleshooting

### "Port 3000 is already in use"
```bash
# macOS/Linux - find and kill process
lsof -i :3000
kill -9 <PID>

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### "Connection refused" (Backend)
- Check PostgreSQL is running
- Check DATABASE_URL in backend/.env
- Make sure you created the database: `createdb edu_platform`

### "Cannot find module" (Frontend)
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### "psql: command not found"
- PostgreSQL not installed or not in PATH
- Try: `/usr/local/opt/postgresql@15/bin/psql` (macOS)
- Or reinstall PostgreSQL

---

## 📚 Learn More

- Backend: Read [backend/README.md](backend/README.md)
- Deployment: Read [DEPLOYMENT.md](DEPLOYMENT.md)
- Full docs: Read [README.md](README.md)

---

## ✨ What You Can Do

### As a Student
1. Sign up with email & password
2. Browse available courses
3. Click "Enroll Now" to join courses
4. See your enrollments

### As an Admin
1. Sign up as Admin (during signup, select Admin role)
2. Add new courses (name, description, instructor)
3. View all student enrollments in table
4. Delete courses if needed

---

## 🎯 Next Steps

1. Run the application locally
2. Test all features
3. Deploy to production (see DEPLOYMENT.md)
4. Add more features (see README.md "Next Steps")

Happy learning! 📚
