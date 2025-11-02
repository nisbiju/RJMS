# 🚀 RJMS Quick Start

## The app is ready! Here's how to run it:

### **Option 1: Using Node.js** (Easiest)
Open the Shell and run:
```bash
node start_services.js
```

### **Option 2: Using Bash Script**
Open the Shell and run:
```bash
./run_rjms.sh
```

### **Option 3: Manual (Two Shell Tabs)**

**Shell Tab 1 - Backend:**
```bash
cd backend
python run.py
```

**Shell Tab 2 - Frontend:**
```bash
npx vite --host 0.0.0.0 --port 5173
```

---

## ✅ Once Running:

1. Click the **Webview** tab in Replit
2. The home page should load
3. Click the **"Login"** button in the navigation
4. Choose **"Student"** or **"Teacher"** from the dropdown
5. Enter any email and name on the login page
6. You'll be redirected to the respective dashboard!

---

## 🎯 What's Implemented:

✓ Home page with Login dropdown (Student/Teacher)  
✓ Separate login pages for Student and Teacher  
✓ "Sign in with Google (Demo Mode)" button  
✓ Full Student dashboard and features  
✓ Full Teacher dashboard and features  
✓ PostgreSQL database with all tables  
✓ Complete Flask API backend  
✓ Vue.js frontend with routing  
✓ Your exact color palette (#FFF7ED, #FBEAD3, #F9DDBB, #C4B49E)

---

## 🧪 Test Accounts:

**Student:**
- Email: student@test.com
- Name: Test Student

**Teacher:**
- Email: teacher@test.com
- Name: Test Teacher

---

**Need help?** Make sure both the backend (port 5000) and frontend (port 5173) are running.
