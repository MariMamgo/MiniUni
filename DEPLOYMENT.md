# Complete Deployment Guide

## Option 1: Deploy on Render + Vercel (Recommended - FREE TIER)

### Step 1: Prepare GitHub Repository

```bash
cd /Users/mamgo/Desktop/website\ for\ mini\ uni
git init
git add .
git commit -m "Initial commit"
git branch -M main
# Push to GitHub (create repo first)
git remote add origin https://github.com/YOUR_USERNAME/edu-platform.git
git push -u origin main
```

### Step 2: Deploy PostgreSQL on Render

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New+" → "PostgreSQL"
4. Fill in:
   - **Name**: edu-platform-db
   - **Database**: edu_platform
   - **User**: postgres
   - **Region**: Choose closest to you
5. Click "Create Database"
6. Copy the **Internal Database URL** (you'll need this)

### Step 3: Deploy Backend on Render

1. Go to https://render.com
2. Click "New+" → "Web Service"
3. Connect GitHub and select your repository
4. Fill in:
   - **Name**: edu-platform-api
   - **Region**: Same as database
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt && pip install gunicorn`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Root Directory**: backend

5. Click "Create Web Service"

6. Once created, go to **Environment** and add variables:
   ```
   DATABASE_URL = (paste the URL from PostgreSQL)
   SECRET_KEY = (generate with: python -c "import secrets; print(secrets.token_hex(32))")
   FLASK_ENV = production
   ```

7. Copy your backend URL (e.g., https://edu-platform-api.onrender.com)

### Step 4: Deploy Frontend on Vercel

1. Go to https://vercel.com
2. Sign in with GitHub
3. Click "Add New" → "Project"
4. Select your repository
5. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: frontend
   - **Build Command**: `npm run build`
   - **Output Directory**: dist
   - **Install Command**: `npm install`

6. Click "Deploy"

7. After deployment, go to **Settings** → **Environment Variables**
   - Add: `VITE_API_URL` = (your backend Render URL)

8. Redeploy to apply environment variables

### Step 5: Update Frontend API Configuration

In `frontend/src/pages/LoginPage.jsx`, `StudentDashboard.jsx`, and `AdminDashboard.jsx`, update API calls:

```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Change all axios calls from '/api' to:
axios.get(`${API_URL}/auth/login`, ...)
```

---

## Option 2: Deploy on Railway (Alternative - Even Easier)

### Railway Setup (Full Stack)

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "PostgreSQL" template
5. Click "Deploy"

6. Go to your project and click "New"
7. Select "GitHub Repo"
8. Choose your repository

9. For Backend service:
   - Link repo to backend folder
   - Add variables:
     ```
     DATABASE_URL = (from PostgreSQL service)
     SECRET_KEY = (generate one)
     FLASK_ENV = production
     PORT = 8000
     ```

10. For Frontend service:
    - Link repo to frontend folder
    - Add build command: `npm install && npm run build`
    - Add environment: `VITE_API_URL = (backend Railway URL)`

---

## Option 3: Free Alternatives for Database

### Using SQLite (No separate database needed)

For testing/development, you can use SQLite instead of PostgreSQL:

1. Update `backend/.env`:
   ```
   DATABASE_URL = sqlite:///edu_platform.db
   ```

2. Update `backend/requirements.txt`:
   ```
   Remove: psycopg2-binary
   Keep everything else
   ```

⚠️ **Note**: SQLite works great for development but has limitations for production with multiple users.

---

## Monitoring & Maintenance

### Check Logs
- **Render**: Services → Select service → Logs tab
- **Railway**: Deploy → Logs tab
- **Vercel**: Deployments → View logs

### Debug Connection Issues

```bash
# Test backend connection
curl https://your-api.onrender.com/api/health

# Check environment variables are set
# In Render/Railway dashboard → Service → Environment
```

### Free Tier Limitations

**Render Free Tier:**
- Services spin down after 15 mins of inactivity
- PostgreSQL: 400 MB storage
- Backend: 0.5 CPU, 512 MB RAM

**Vercel Free Tier:**
- Up to 100 GB bandwidth
- Fast deployments
- Automatic HTTPS

---

## Cost Breakdown (Starting Month)

| Service | Plan | Cost |
|---------|------|------|
| Render PostgreSQL | Free | $0 |
| Render Backend | Free | $0 |
| Vercel Frontend | Free | $0 |
| **Total** | | **$0** |

After usage increases (optional upgrades):
- Render PostgreSQL Pro: $15/month
- Render Backend Pro: $12/month
- Vercel Pro: $20/month

---

## Common Issues & Fixes

### "Connection refused" error
```bash
# Check if database is running in Render console
# Restart service: Settings → Restart Service
```

### CORS errors
Add to `backend/app.py`:
```python
CORS(app, origins=["https://your-vercel-url.vercel.app"])
```

### Frontend can't reach API
1. Verify `VITE_API_URL` environment variable is set
2. Check backend is actually running (curl the health endpoint)
3. Ensure no firewall blocking

### Database migrations
```bash
# SSH into Render backend
# Run: python app.py
# This will auto-create tables
```

---

## Production Checklist

- [ ] Change `SECRET_KEY` to secure random value
- [ ] Set `FLASK_ENV = production`
- [ ] Enable HTTPS (automatic on Render/Vercel)
- [ ] Configure CORS for your domain
- [ ] Set up error logging
- [ ] Test with real data
- [ ] Add rate limiting
- [ ] Backup database regularly

---

## Getting Help

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Flask**: https://flask.palletsprojects.com
- **React**: https://react.dev

Happy deploying! 🚀
