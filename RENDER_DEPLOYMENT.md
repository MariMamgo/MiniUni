# Deployment Instructions for Render.com

## Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub account

## Step 2: Deploy Backend
1. Click "New +"
2. Select "Web Service"
3. Connect your GitHub repo (MariMamgo/MiniUni)
4. Fill in:
   - Name: `miniuni-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && python3 app.py`
   - Runtime: `Python 3`

5. Click "Advanced" and add Environment Variables:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=<Will be provided by Render PostgreSQL>
   ```

6. Add PostgreSQL Database:
   - Click "Create +" > "PostgreSQL"
   - Name: `miniuni-db`
   - Render will provide DATABASE_URL automatically

## Step 3: Deploy Frontend
1. Click "New +"
2. Select "Static Site"
3. Connect GitHub repo
4. Fill in:
   - Name: `miniuni-frontend`
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`

5. Add Environment Variable:
   ```
   VITE_API_URL=https://miniuni-backend.onrender.com
   ```

## Step 4: Update Code
After deployment, update frontend API URL:
- Change `http://localhost:5001` to your Render backend URL in `frontend/src/api/axiosConfig.js`

## Your URLs will be:
- Backend: https://miniuni-backend.onrender.com
- Frontend: https://miniuni-frontend.onrender.com

## First Deploy Notes:
- First deploy takes 5-10 minutes
- Database initializes automatically
- Courses and admin account will be created on first run
