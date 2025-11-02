# 🚀 Quick Start Guide for RJMS

Your application is ready! Follow these simple steps to run it:

## Option 1: Automated Start (Recommended)

Open the Shell and run:
```bash
./run_rjms.sh
```

This will start both the backend and frontend automatically.

## Option 2: Manual Start

If the automated script doesn't work, open **TWO** separate Shell tabs:

### Shell Tab 1 - Backend
```bash
cd backend
python run.py
```

Wait until you see: `Running on http://127.0.0.1:5000`

### Shell Tab 2 - Frontend
```bash
cd frontend
npm run dev
```

Wait until you see the local URL (usually `http://localhost:5173`)

## 🌐 Access the Application

Once both services are running:
1. Click the **"Open in a new tab"** button in the Webview
2. Or click the **Webview** tab in Replit

## 🧪 Test the Login Flow

1. On the home page, click the **"Login"** button in the navigation bar
2. Select either **"Student"** or **"Teacher"** from the dropdown
3. You'll land on a dedicated login page
4. Enter any email and name (e.g., `test@example.com`, `John Doe`)
5. Click **"Sign in with Google (Demo Mode)"**
6. You'll be redirected to the respective dashboard!

### Student Login Test:
- Email: `student@test.com`
- Name: `Test Student`

### Teacher Login Test:
- Email: `teacher@test.com`
- Name: `Test Teacher`

## ✅ What's Working

- ✓ Home page with Login dropdown (Student/Teacher options)
- ✓ Dedicated Student login page (`/login/student`)
- ✓ Dedicated Teacher login page (`/login/teacher`)
- ✓ Google OAuth demo mode
- ✓ Student dashboard and all features
- ✓ Teacher dashboard and all features
- ✓ PostgreSQL database with all tables
- ✓ Full API backend with Flask

## 🎨 Design

The application uses your exact color palette:
- Background: `#FFF7ED`
- Containers: `#FBEAD3`
- Buttons/Popups: `#F9DDBB`
- Filters: `#C4B49E`

## 📚 Full Documentation

See `README.md` for complete documentation including:
- API endpoints
- Database schema
- Feature list
- Production deployment guide

---

**Need help?** Check that both services (backend and frontend) are running in separate Shell tabs.
