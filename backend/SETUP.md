# FinSphere Backend Setup Guide

## Quick Start (15 minutes)

### Step 1: Create Virtual Environment

```bash
cd "D:\My Projects\FinSphere\backend"
python -m venv venv
```

### Step 2: Activate Virtual Environment

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**If you get execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

**Copy `.env.example` to `.env`:**
```powershell
Copy-Item .env.example .env
```

**Edit `.env` file** and update:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/finsphere_dev
SECRET_KEY=your-super-secret-key-change-this-in-production
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

### Step 5: Set Up Database

**Create database:**
```powershell
# Open PostgreSQL command line or use pgAdmin
createdb finsphere_dev

# Or in psql:
psql -U postgres
CREATE DATABASE finsphere_dev;
\q
```

**Load schema and seed data:**
```powershell
cd "D:\My Projects\FinSphere"
psql -U postgres -d finsphere_dev -f database/schema.sql
psql -U postgres -d finsphere_dev -f database/seeds/01_learning_content.sql
psql -U postgres -d finsphere_dev -f database/seeds/02_sample_assets.sql
```

### Step 6: Run the Backend

```bash
cd backend
uvicorn app.main:app --reload
```

**You should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Step 7: Test the API

Open your browser and go to:
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## Testing Authentication

### Register a User

**Using the /docs interface:**
1. Go to http://localhost:8000/docs
2. Click on **POST /api/auth/register**
3. Click **Try it out**
4. Enter:
```json
{
  "email": "test@example.com",
  "password": "testpassword123",
  "full_name": "Test User",
  "knowledge_level": "beginner"
}
```
5. Click **Execute**

### Login

1. Click on **POST /api/auth/login**
2. Click **Try it out**
3. Enter:
```json
{
  "email": "test@example.com",
  "password": "testpassword123"
}
```
4. Click **Execute**
5. Copy the `access_token` from the response

### Test Protected Route

1. Click the **Authorize** button (🔒) at the top
2. Paste your token
3. Try **GET /api/auth/me** to see your user info

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   └── auth.py          # Authentication routes
│   ├── core/                # Core functionality
│   │   ├── __init__.py
│   │   └── security.py      # Password hashing, JWT
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py
│   └── schemas/             # Pydantic schemas
│       ├── __init__.py
│       └── user.py
├── venv/                    # Virtual environment (created by you)
├── .env                     # Environment variables (created by you)
├── .env.example             # Example environment file
└── requirements.txt         # Python dependencies
```

---

## Common Issues & Solutions

### Issue: "psql: command not found"
**Solution:** Add PostgreSQL to PATH or use full path:
```powershell
& "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres -d finsphere_dev
```

### Issue: "Connection refused" when connecting to database
**Solutions:**
1. Make sure PostgreSQL is running
2. Check your DATABASE_URL in `.env`
3. Verify PostgreSQL port (default 5432)

### Issue: Import errors
**Solution:** Make sure virtual environment is activated:
```powershell
.\venv\Scripts\Activate.ps1
```

### Issue: "Table already exists"
**Solution:** Database was already created. Either:
- Drop and recreate: `dropdb finsphere_dev && createdb finsphere_dev`
- Or continue using existing database

---

## What's Included

✅ **FastAPI application** with automatic API documentation  
✅ **PostgreSQL connection** via SQLAlchemy ORM  
✅ **User authentication** (register + login)  
✅ **JWT token system** for secure API access  
✅ **Password hashing** with bcrypt  
✅ **CORS configuration** for frontend integration  
✅ **Environment configuration** with .env support  

---

## Next Steps (Day 2)

Tomorrow we'll add:
- Learning APIs (courses, lessons, progress)
- Asset APIs (browse stocks, prices)
- Portfolio APIs (create, view holdings)
- Trading APIs (buy, sell stocks)

---

## Quick Commands Reference

```bash
# Activate venv
.\venv\Scripts\Activate.ps1

# Run server
uvicorn app.main:app --reload

# Run server on different port
uvicorn app.main:app --reload --port 8080

# Deactivate venv
deactivate

# Install new package
pip install package-name
pip freeze > requirements.txt
```

---

**Backend Status:** ✅ Authentication Complete  
**Next:** Core API endpoints (Day 2)
