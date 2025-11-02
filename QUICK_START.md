# 🚀 RJMS Quick Start Guide

## Tech Stack (As Specified)
- **Frontend**: Vue.js 3 with Vue Router
- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Note**: Vue.js requires Node.js to run its Vite dev server (this is standard for all Vue.js apps)

---

## How to Run the Application

### **Option 1: Using Python Launcher (Recommended)**

Open the Shell and run:
```bash
python start_app.py
```

This Python script will:
1. Start the Flask backend on port 5000
2. Start the Vue.js frontend (via Vite) on port 5173
3. Display logs from both services

### **Option 2: Manual Start (Two Shell Tabs)**

**Shell Tab 1 - Flask Backend:**
```bash
cd backend
python run.py
```
Wait until you see: `Running on http://127.0.0.1:5000`

**Shell Tab 2 - Vue.js Frontend:**
```bash
cd frontend
npm run dev
```
Wait until you see: `Local: http://localhost:5173/`

---

## ✅ Access the Application

1. Open the **Webview** tab in Replit (or click "Open in new tab")
2. The home page should load
3. Click the **"Login"** button in the navigation bar
4. Choose **"Student"** or **"Teacher"** from the dropdown
5. You'll land on a dedicated login page
6. Enter any email and name (demo mode)
7. Click **"Sign in with Google (Demo Mode)"**
8. You'll be redirected to the respective dashboard!

---

## 🧪 Test the Login Flow

### Student Login:
1. Home page → Click "Login" → Select "Student"
2. Lands on `/login/student`
3. Enter: `student@test.com` / `Test Student`
4. Click "Sign in with Google (Demo Mode)"
5. Redirected to Student dashboard

### Teacher Login:
1. Home page → Click "Login" → Select "Teacher"
2. Lands on `/login/teacher`
3. Enter: `teacher@test.com` / `Test Teacher`
4. Click "Sign in with Google (Demo Mode)"
5. Redirected to Teacher dashboard

---

## 📋 What's Implemented

✅ **Home Page**
- Product, Features, About Us sections
- Navigation with Login dropdown (Student/Teacher)

✅ **Authentication Flow**
- Separate login pages for Student (`/login/student`) and Teacher (`/login/teacher`)
- "Sign in with Google (Demo Mode)" button on each
- Google OAuth demo mode (just enter email and name)
- Session management

✅ **Student Features**
- View enrolled courses
- Access reflection journals
- Submit reflections
- View teacher feedback
- Dashboard with due/overdue reflections
- Profile page

✅ **Teacher Features**
- Create and manage courses
- Configure reflection frameworks (Bloom's Taxonomy, 5 WHYs, 1-H)
- Set course dates and recurrence
- Manage student enrollments
- View all reflection submissions
- Assign scores and approve AI feedback
- Course overview statistics

✅ **Design**
- Desktop-optimized interface
- Exact color palette:
  - Background: `#FFF7ED`
  - Containers: `#FBEAD3`
  - Buttons/Popups: `#F9DDBB`
  - Filters: `#C4B49E`

---

## 🗄️ Database Schema

PostgreSQL tables:
- **users** - Students and teachers with Google OAuth
- **courses** - Course information and configuration
- **enrollments** - Student-course relationships
- **reflections** - Journal assignments with deadlines
- **reflection_submissions** - Student work with feedback and scores

---

## 🔧 Troubleshooting

**App won't start:**
- Ensure PostgreSQL is running (Replit handles this automatically)
- Check that both backend (5000) and frontend (5173) ports are free

**Backend errors:**
- Check `/tmp/backend.log` if using the Python launcher
- Verify DATABASE_URL environment variable is set

**Frontend not loading:**
- Frontend dependencies should auto-install via Replit
- If issues persist, the packager tool will reinstall them

**Login not working:**
- Demo mode doesn't require real Google OAuth
- Just enter any email and name to test

---

## 📚 Full Documentation

See `README.md` for complete documentation including:
- Complete API endpoint reference
- Database schema details
- Production deployment guide
- Google OAuth setup for production

---

**Need help?** Make sure `start_app.py` is running or both services are running in separate shells.
