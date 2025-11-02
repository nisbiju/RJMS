# RJMS - Reflection Journal Management System

A comprehensive web application for managing educational reflection journals, designed for both teachers and students.

## Tech Stack

- **Frontend**: Vue.js 3 with Vue Router
- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Authentication**: Google OAuth (Demo mode included)

## Color Palette

- Background: `#FFF7ED`
- Containers: `#FBEAD3`
- Pop-up/Buttons: `#F9DDBB`
- Course Filter: `#C4B49E`

## Features

### For Students
- View enrolled courses
- Access reflection journals with deadlines
- Submit reflections
- View AI-generated feedback (when approved by teacher)
- Dashboard with due/overdue assignments
- Profile management

### For Teachers
- Create and manage courses
- Configure reflection frameworks (Bloom's Taxonomy, 5 WHYs, 1-H)
- Manage student enrollments
- View reflection submissions
- Provide scores and approve AI feedback
- Course overview and analytics

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL database (automatically provided by Replit)

### 1. Environment Variables

The following environment variables are already configured in Replit:
- `DATABASE_URL` - PostgreSQL connection string
- `SESSION_SECRET` - Flask session secret key

For Google OAuth in production, you'll need to add:
- `GOOGLE_CLIENT_ID` - Your Google OAuth Client ID
- `GOOGLE_CLIENT_SECRET` - Your Google OAuth Client Secret

**Note**: The app currently runs in **demo mode** which allows you to login without actual Google OAuth credentials. Simply enter your email and name to test the application.

### 2. Install Dependencies

#### Backend (Python/Flask)
```bash
cd backend
pip install -r requirements.txt
```

Dependencies are automatically installed by Replit when you use the packager tool.

#### Frontend (Vue.js)
```bash
cd frontend
npm install
```

### 3. Database Setup

The PostgreSQL database is automatically created by Replit. The Flask application will create all necessary tables on first run.

### 4. Running the Application

#### Development Mode

**Option 1: Using the provided startup script (Recommended)**
```bash
chmod +x start.sh
./start.sh
```

This will start both the Flask backend (port 5000) and Vue.js frontend (port 5173).

**Option 2: Run manually**

Terminal 1 - Backend:
```bash
cd backend
python run.py
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

### 5. Accessing the Application

- Frontend: http://localhost:5173 (or Replit webview)
- Backend API: http://localhost:5000/api

## Application Structure

```
.
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   └── models.py          # Database models
│   │   ├── routes/
│   │   │   ├── auth.py            # Authentication routes
│   │   │   ├── courses.py         # Course management
│   │   │   ├── students.py        # Student management
│   │   │   ├── teacher.py         # Teacher-specific routes
│   │   │   └── reflections.py     # Reflection journal routes
│   │   ├── utils/
│   │   │   └── auth_utils.py      # Authentication utilities
│   │   └── __init__.py            # Flask app factory
│   └── run.py                      # Application entry point
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   │   └── main.css           # Global styles with color palette
│   │   ├── components/            # Reusable Vue components
│   │   ├── router/
│   │   │   └── index.js           # Vue Router configuration
│   │   ├── views/
│   │   │   ├── Home.vue           # Landing page
│   │   │   ├── StudentLogin.vue   # Student login
│   │   │   ├── TeacherLogin.vue   # Teacher login
│   │   │   ├── student/           # Student views
│   │   │   │   ├── StudentHome.vue
│   │   │   │   ├── StudentCourse.vue
│   │   │   │   ├── StudentDashboard.vue
│   │   │   │   ├── StudentProfile.vue
│   │   │   │   └── ReflectionDetails.vue
│   │   │   └── teacher/           # Teacher views
│   │   │       ├── TeacherHome.vue
│   │   │       ├── CourseOverview.vue
│   │   │       ├── CourseConfiguration.vue
│   │   │       ├── ManageStudents.vue
│   │   │       ├── CourseReflections.vue
│   │   │       └── ReflectionSubmissions.vue
│   │   ├── App.vue                # Root component
│   │   └── main.js                # Application entry point
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
└── README.md
```

## Using the Application

### First Time Setup

1. **Access the Home Page**: Navigate to the root URL to see the landing page with Product, Features, and About Us sections.

2. **Login**: Click the "Login" dropdown button in the navigation bar and choose either:
   - **Student** - For student access
   - **Teacher** - For teacher access

3. **Demo Mode**: Enter any email and name to login (no Google account required in demo mode)

### As a Teacher

1. **Create a Course**:
   - Click "Add New Course" on the teacher home page
   - Enter course name and optional course code
   - Click "Create Course"

2. **Configure Course**:
   - Click on a course to view details
   - Navigate to "Configure" from the side panel
   - Set reflection framework, dates, recurrence, and days
   - Click "Submit Configuration"

3. **Manage Students**:
   - Navigate to "Manage Students" from the side panel
   - Click "Add Student" and enter student email
   - Select multiple students and delete if needed

4. **View Reflections**:
   - Navigate to "Reflections" from the side panel
   - Click on a reflection to view all student submissions
   - Enter scores and approve AI feedback for students

### As a Student

1. **View Courses**:
   - See all enrolled courses on the student home page
   - Use search and filters to find specific courses

2. **Access Reflections**:
   - Click on a course to see all reflection journals
   - Click on a reflection to view details and submit

3. **Submit Reflection**:
   - Write your reflection in the text area
   - Click "Submit" to save your work
   - View teacher feedback when available

4. **Dashboard**:
   - Click "Dashboard" to see all due and overdue reflections
   - Sort by dates or courses
   - Click on any reflection to navigate directly to it

## API Endpoints

### Authentication
- `POST /api/auth/google` - Google OAuth login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user

### Courses
- `GET /api/courses` - Get all courses (filtered by role)
- `GET /api/courses/:id` - Get course details
- `POST /api/courses` - Create new course (teacher only)
- `PUT /api/courses/:id/configure` - Configure course (teacher only)

### Students
- `GET /api/students/course/:courseId` - Get course students (teacher only)
- `POST /api/students/course/:courseId` - Add student to course (teacher only)
- `DELETE /api/students/:studentId/course/:courseId` - Remove student (teacher only)

### Reflections
- `GET /api/reflections/course/:courseId` - Get course reflections
- `GET /api/reflections/:id` - Get reflection details
- `POST /api/reflections/submit` - Submit reflection (student only)
- `GET /api/reflections/:id/submissions` - Get all submissions (teacher only)
- `PUT /api/reflections/submission/:id/update` - Update score/feedback (teacher only)
- `GET /api/reflections/dashboard` - Get student dashboard (student only)

### Teacher
- `GET /api/teacher/course/:courseId/overview` - Get course overview stats (teacher only)

## Production Deployment

### Google OAuth Setup

To enable real Google OAuth in production:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://localhost:5000/api/auth/google/callback` (development)
   - `https://your-domain.com/api/auth/google/callback` (production)
6. Set environment variables:
   ```
   GOOGLE_CLIENT_ID=your_client_id
   GOOGLE_CLIENT_SECRET=your_client_secret
   ```
7. Update `backend/app/routes/auth.py` to use real Google token verification

### Security Considerations

- Change `SECRET_KEY` to a strong random value in production
- Enable HTTPS for all production traffic
- Use environment variables for all sensitive data
- Implement rate limiting on API endpoints
- Add CSRF protection for forms
- Enable database backups
- Implement proper error logging

## Troubleshooting

### Backend Issues

**Database connection error**:
- Verify `DATABASE_URL` environment variable is set
- Check PostgreSQL is running
- Verify database credentials

**Import errors**:
- Run `pip install -r requirements.txt` in backend directory
- Check Python version is 3.11+

### Frontend Issues

**Module not found**:
- Run `npm install` in frontend directory
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`

**API connection error**:
- Ensure backend is running on port 5000
- Check Vite proxy configuration in `frontend/vite.config.js`

**Build errors**:
- Clear Vite cache: `rm -rf frontend/.vite`
- Rebuild: `npm run build`

## Team

RJMS was developed by:
- Nisha
- Hamid
- Tanvi
- Kushal
- Vinay

Under the guidance of Professor Shashi Kant Shankar, Ahmedabad University.

## License

This project was developed as part of coursework at IIT Bombay.

## Support

For issues or questions, please contact the development team or refer to the project documentation.
