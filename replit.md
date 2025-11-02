# RJMS - Reflection Journal Management System

## Overview

RJMS is an educational web application that enables structured reflection journaling for students and teachers. The system supports multiple reflection frameworks (Bloom's Taxonomy, 5 WHYs, 1-H), manages course enrollments, handles reflection submissions, and provides AI-generated feedback mechanisms. Teachers can create courses with configurable reflection schedules, while students submit reflections and receive feedback.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Stack:**
- Vue.js 3 with Composition API
- Vue Router for client-side routing
- Axios for HTTP requests
- Vite as build tool and dev server

**Design Decisions:**
- **Component-Based Architecture**: The application uses Vue's component system to organize UI into reusable pieces separated by user role (student/teacher views)
- **Route-Based Code Splitting**: Router configuration splits views into student and teacher sections with role-based access control using route meta fields
- **Proxy Configuration**: Vite dev server proxies `/api` requests to the Flask backend (port 5001), enabling seamless local development without CORS issues
- **Custom CSS Variables**: Uses a custom color palette defined in CSS variables for consistent theming across the application

**Port Configuration:**
- Frontend runs on port 5173 (Vite default)
- Note: There's a discrepancy in vite.config.js (shows port 5000) vs standard Vite setup

### Backend Architecture

**Technology Stack:**
- Flask (Python) web framework
- Flask-SQLAlchemy ORM
- Flask-CORS for cross-origin requests
- PostgreSQL database

**Design Decisions:**
- **Blueprint-Based Routing**: API routes are organized into logical blueprints (auth, courses, students, teacher, reflections) for modularity and maintainability
- **Session-Based Authentication**: Uses Flask sessions for user authentication state management instead of JWT tokens
- **Decorator-Based Authorization**: Custom decorators (`@login_required`, `@teacher_required`, `@student_required`) enforce role-based access control at the route level
- **SQLAlchemy Models**: Database schema defined using SQLAlchemy ORM with relationships between User, Course, Enrollment, Reflection, and ReflectionSubmission entities
- **Demo Mode Support**: Google OAuth integration includes demo/development mode bypassing actual token verification for easier testing

**API Structure:**
- `/api/auth/*` - Authentication endpoints
- `/api/courses/*` - Course management
- `/api/students/*` - Student enrollment operations
- `/api/teacher/*` - Teacher-specific analytics and overview
- `/api/reflections/*` - Reflection submission and retrieval

**Port Configuration:**
- Backend runs on port 5001 (configurable via PORT environment variable)

### Database Schema

**Core Entities:**

1. **Users** - Stores both students and teachers with role differentiation
   - Fields: id, email, name, google_id, role, profile_image, created_at
   - Role can be 'student' or 'teacher'

2. **Courses** - Teacher-created courses with reflection configuration
   - Fields: id, name, course_code, teacher_id, status, framework, start_date, end_date, reflection_due_days, recurrence_days, selected_days, custom_structure
   - Supports multiple reflection frameworks and custom structures (stored as JSON)

3. **Enrollments** - Many-to-many relationship between students and courses
   - Fields: id, student_id, course_id, enrolled_at

4. **Reflections** - Individual reflection assignments within courses
   - Fields: id, course_id, name, number, description, start_date, due_date, structure

5. **ReflectionSubmissions** - Student submissions with feedback
   - Fields: id, reflection_id, student_id, content, submitted_at, ai_feedback, display_feedback, teacher_score

**Relationships:**
- One-to-many: Teacher → Courses
- Many-to-many: Students ↔ Courses (via Enrollments)
- One-to-many: Course → Reflections
- One-to-many: Reflection → Submissions
- Cascade deletes configured for course-related entities

### Authentication & Authorization

**OAuth Integration:**
- Google OAuth 2.0 for user authentication
- Development mode allows bypassing real Google verification
- Session-based state management stores user_id and role

**Access Control:**
- Role-based access at route level using decorators
- Session validation on protected endpoints
- Teacher-student data isolation (teachers only access their courses, students only their enrollments)

## External Dependencies

### Third-Party Services

1. **Google OAuth 2.0**
   - Purpose: User authentication
   - Configuration: Requires GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables
   - Demo mode available for development

2. **PostgreSQL Database**
   - Purpose: Primary data store
   - Configuration: DATABASE_URL environment variable (auto-provisioned on Replit)
   - ORM: SQLAlchemy

### Frontend Dependencies

- **vue** (^3.5.13) - Core framework
- **vue-router** (^4.5.0) - Client-side routing
- **axios** (^1.7.9) - HTTP client
- **@vitejs/plugin-vue** - Vite integration
- **vite** (^5.4.20) - Build tool and dev server

### Backend Dependencies

- **Flask** - Web framework
- **Flask-SQLAlchemy** - Database ORM
- **Flask-CORS** - Cross-origin resource sharing
- **google-auth** - OAuth token verification (for production)

### Development Tools

- **Drizzle Kit** - Database migration tool (configured but may not be actively used with Flask-SQLAlchemy)
- **PostCSS** with Autoprefixer - CSS processing
- **TailwindCSS** - Utility-first CSS framework (configured via components.json)

### Environment Variables Required

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Flask session secret
- `GOOGLE_CLIENT_ID` - OAuth client ID
- `GOOGLE_CLIENT_SECRET` - OAuth client secret
- `PORT` - Backend server port (defaults to 5001)