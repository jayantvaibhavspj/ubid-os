# UBID-OS Setup Guide

Complete step-by-step setup instructions for the UBID-OS platform.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Docker Setup (Recommended)](#docker-setup)
3. [Local Development Setup](#local-development-setup)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **RAM**: 4GB
- **Disk**: 2GB free space
- **CPU**: 2 cores

### Recommended Requirements
- **RAM**: 8GB
- **Disk**: 5GB free space
- **CPU**: 4 cores

---

## Docker Setup (Recommended)

### Prerequisites
1. **Install Docker Desktop**
   - Windows/macOS: Download from https://www.docker.com/products/docker-desktop
   - Linux: `curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh`

2. **Verify Installation**
   ```bash
   docker --version
   docker-compose --version
   ```

### Step-by-Step Setup

#### Step 1: Navigate to Project Directory
```bash
cd ubid-os
```

#### Step 2: Build Docker Images
```bash
docker-compose build
```

This will:
- Build Python backend image with all dependencies
- Build Node.js frontend image with all packages
- Estimated time: 5-10 minutes (first run)

#### Step 3: Start Services
```bash
docker-compose up
```

Output should show:
```
backend_1   | INFO:     Uvicorn running on http://0.0.0.0:8000
frontend_1  | Compiled successfully!
```

#### Step 4: Access Application
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

#### Step 5: Stop Services
```bash
docker-compose down
```

---

## Local Development Setup

### Backend Setup

#### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

#### Step 1: Create Virtual Environment
```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Expected packages:
- fastapi==0.109.0
- uvicorn==0.27.0
- sqlalchemy==2.0.25
- jellyfish==1.0.3
- pandas==2.1.4
- faker==22.0.0
- ... and more

#### Step 3: Run Backend Server
```bash
uvicorn app.main:app --reload
```

Output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

#### Step 4: Verify API
Open http://localhost:8000/docs in browser to see interactive API documentation.

### Frontend Setup

#### Prerequisites
- Node.js 18 or higher
- npm (Node package manager)

#### Step 1: Navigate to Frontend Directory
```bash
cd frontend
```

#### Step 2: Install Dependencies
```bash
npm install
```

This installs:
- react@18.2.0
- tailwindcss@3.4.1
- axios@1.6.5
- recharts@2.10.3
- ... and more

#### Step 3: Start Development Server
```bash
npm start
```

Output:
```
Compiled successfully!
You can now view ubid-os-frontend in the browser.
Local: http://localhost:3000
```

Application will automatically open in your default browser.

---

## Configuration

### Environment Variables

#### Backend (.env)
Create `backend/.env`:
```env
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Database (not used in demo, but included for future)
DATABASE_URL=sqlite:///./test.db

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

#### Frontend (.env.local)
Create `frontend/.env.local`:
```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_TIMEOUT=30000

# Analytics (optional)
REACT_APP_ANALYTICS_ID=
```

### Docker Compose Configuration

Edit `docker-compose.yml` to customize:

```yaml
# Port mappings
ports:
  - "8000:8000"  # Backend
  - "3000:3000"  # Frontend

# Volume mounts for hot reload
volumes:
  - ./backend/app:/app/app
  - ./frontend/src:/app/src
```

---

## Running the Application

### First-Time Setup Checklist

- [ ] Docker Desktop running (if using Docker)
- [ ] Port 3000 available (frontend)
- [ ] Port 8000 available (backend)
- [ ] Internet connection for npm/pip downloads
- [ ] At least 4GB RAM available

### Common Startup Scenarios

#### Scenario 1: Fresh Start with Docker
```bash
docker-compose down --volumes  # Clean slate
docker-compose build --no-cache  # Fresh build
docker-compose up                # Start
```

#### Scenario 2: Quick Restart
```bash
docker-compose restart
```

#### Scenario 3: View Logs
```bash
docker-compose logs -f backend   # Backend logs
docker-compose logs -f frontend  # Frontend logs
docker-compose logs -f           # All logs
```

#### Scenario 4: Local Development with Hot Reload
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 0.0.0.0

# Terminal 2: Frontend
cd frontend
npm start
```

---

## Initialization Process

### What Happens on Startup

1. **Backend Initialization** (first API call)
   ```
   Generating synthetic dataset...
   Generated 900 department records
   Created 280 UBIDs
   Classified 280 businesses
   System ready
   ```

2. **Data Included**
   - 200 active businesses
   - 50 ghost businesses
   - 30 dormant businesses
   - 4 department systems
   - ~900 total records

3. **Time to Ready**: ~2 seconds

### Accessing the Dashboard

1. Open http://localhost:3000 in browser
2. See initialization notification (if first run)
3. Dashboard loads with:
   - System statistics
   - Business status distribution
   - Ghost business count
   - Pending review queue

---

## Troubleshooting

### Issue: Port Already in Use

**Problem**: Error "Address already in use"

**Solution**:
```bash
# Find process using port 3000 (frontend)
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Kill process or use different port
docker-compose down
# OR change port in docker-compose.yml

ports:
  - "3001:3000"  # Use 3001 instead
```

### Issue: Backend Connection Refused

**Problem**: Frontend can't connect to backend at http://localhost:8000

**Solution**:
1. Verify backend is running: http://localhost:8000/docs
2. Check CORS settings in `backend/app/main.py`
3. Clear browser cache (Ctrl+Shift+Delete)
4. Check firewall settings

### Issue: Docker Build Fails

**Problem**: Docker build fails with dependency errors

**Solution**:
```bash
# Clean build
docker-compose build --no-cache

# Check logs
docker-compose logs backend

# Restart Docker daemon
# Windows/macOS: Restart Docker Desktop
# Linux: sudo systemctl restart docker
```

### Issue: npm or pip Dependencies Fail

**Problem**: Dependency installation fails

**Solution**:
```bash
# Backend
pip install --upgrade pip
pip cache purge
pip install -r requirements.txt --no-cache-dir

# Frontend
npm cache clean --force
npm install --legacy-peer-deps
```

### Issue: Slow Performance

**Problem**: Application is slow or laggy

**Reasons & Solutions**:
- Low RAM: Close other applications, allocate more to Docker
- Slow disk: SSD recommended for Docker Desktop
- Network: Ensure stable internet connection
- Database: Current in-memory DB is fast; future PostgreSQL needed for production

### Issue: Data Not Loading

**Problem**: Dashboard shows empty data

**Solution**:
1. Clear browser cache
2. Hard refresh (Ctrl+F5)
3. Check browser console for errors (F12)
4. Verify backend logs: `docker-compose logs backend`
5. Restart services: `docker-compose restart`

---

## Performance Optimization

### For Development
```yaml
# docker-compose.yml
backend:
  environment:
    - PYTHONUNBUFFERED=1
  command: uvicorn app.main:app --reload --host 0.0.0.0 --workers 1

frontend:
  environment:
    - FAST_REFRESH=true
```

### For Production
```yaml
backend:
  command: uvicorn app.main:app --host 0.0.0.0 --workers 4

frontend:
  command: npm run build && serve -s build
```

---

## Testing the Setup

### Backend Tests

```bash
# Test API is running
curl http://localhost:8000/

# Test statistics endpoint
curl http://localhost:8000/api/statistics

# Test ghost businesses endpoint
curl http://localhost:8000/api/ghost-businesses
```

### Frontend Tests

1. Open http://localhost:3000
2. Navigate through tabs:
   - [ ] Dashboard loads
   - [ ] Ghost Businesses shows list
   - [ ] Entity Resolver accepts input
   - [ ] Query Interface executes queries
   - [ ] Charts render correctly

### Integration Tests

1. In Entity Resolver tab:
   - Enter 2 business names
   - Click "Resolve Entities"
   - Verify matches are returned

2. In Ghost Businesses tab:
   - Verify ghost count > 0
   - Click on a business
   - Modal shows evidence timeline

3. In Query Interface:
   - Execute "All Ghost Businesses" query
   - Export as CSV
   - Verify file downloads

---

## Resetting to Clean State

### Docker
```bash
docker-compose down -v          # Remove volumes
docker volume prune             # Clean up
docker-compose build --no-cache # Rebuild
docker-compose up               # Fresh start
```

### Local Development
```bash
# Backend
rm -rf backend/venv
python -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt

# Frontend
rm -rf frontend/node_modules
npm install --prefix frontend
```

---

## Next Steps

1. **Explore the Dashboard**
   - Review statistics and metrics
   - Understand ghost business detection

2. **Try Entity Resolution**
   - Enter sample business records
   - See how matching algorithm works

3. **Review API Documentation**
   - Visit http://localhost:8000/docs
   - Try different endpoints

4. **Examine Source Code**
   - `backend/app/entity_resolver.py` - Matching engine
   - `backend/app/activity_classifier.py` - Classification logic
   - `frontend/src/components/Dashboard.jsx` - Dashboard component

---

## Getting Help

### Documentation
- README.md - Project overview
- This file - Setup guide
- API Docs - http://localhost:8000/docs
- Source code comments - Well commented for clarity

### Common Resources
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- Docker: https://docs.docker.com/

---

## System Health Check

Run this to verify everything is working:

```bash
# 1. Check services running
docker-compose ps

# 2. Check backend health
curl -s http://localhost:8000/ | jq .

# 3. Check frontend accessibility
curl -s http://localhost:3000 | head -20

# 4. Test entity resolution
curl -X POST http://localhost:8000/api/resolve \
  -H "Content-Type: application/json" \
  -d '{"records": [{"business_name": "Test Inc"}]}'

# 5. Check statistics
curl -s http://localhost:8000/api/statistics | jq .
```

---

**Setup Complete!** 🎉

You're now ready to explore the UBID-OS platform. Start with the Dashboard to see real-time business intelligence data.
