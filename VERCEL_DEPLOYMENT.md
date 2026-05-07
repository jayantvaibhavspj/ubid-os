# Vercel Deployment Guide - UBID-OS

## ✅ Frontend Deployment (React on Vercel)

### Step 1: Connect GitHub Repository
1. Go to https://vercel.com
2. Click "New Project"
3. Select "Import Git Repository"
4. Select `jayantvaibhavspj/ubid-os` repository
5. Choose `frontend` as root directory (if prompted)
6. Click "Deploy"

**Expected Result**: Frontend deployed at `ubid-os.vercel.app` (or similar)

### Step 2: Configure Environment Variables (if needed)
In Vercel Dashboard:
- Settings → Environment Variables
- Add `REACT_APP_API_URL` = your backend API URL

---

## ✅ Backend Deployment (FastAPI on Vercel)

### Step 1: Deploy Backend
1. Go to https://vercel.com
2. Click "New Project"
3. Create new project with GitHub integration
4. Point to `backend` directory
5. Set Python runtime to 3.10
6. Click "Deploy"

**Expected Result**: Backend deployed at `ubid-os-backend.vercel.app` (or similar)

---

## 🔗 Demo Links After Deployment

**Frontend Demo**: `https://ubid-os.vercel.app`
**Backend API**: `https://ubid-os-backend.vercel.app`
**API Docs**: `https://ubid-os-backend.vercel.app/docs`

---

## ⚠️ Important Notes

1. **Database**: Currently using in-memory. For production, set up PostgreSQL
2. **CORS**: Already configured to allow all origins
3. **API Proxy**: Frontend configured to proxy `/api/*` requests to backend
4. **Cold Start**: First request may be slow (serverless cold start)

---

## 🚀 Alternative: Local Demo (If Vercel Not Available)

```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm start
```

**Access**: http://localhost:3000

---

## 📝 Submission with Demo Link

Once deployed, use these links in HackerEarth form:
- **Demo Link**: `https://ubid-os.vercel.app`
- **Repository**: `https://github.com/jayantvaibhavspj/ubid-os`
- **API Docs**: `https://ubid-os-backend.vercel.app/docs`

