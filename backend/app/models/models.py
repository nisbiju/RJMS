from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    google_id = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'student' or 'teacher'
    profile_image = db.Column(db.Text)  # Base64 encoded image
    department = db.Column(db.String(255))
    experience = db.Column(db.String(255))  # For teachers
    area_of_interest = db.Column(db.String(255))
    student_id = db.Column(db.String(100))  # For students
    year_of_joining = db.Column(db.String(50))  # For students
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    courses_taught = db.relationship('Course', backref='teacher', lazy=True, foreign_keys='Course.teacher_id')
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)
    reflections = db.relationship('ReflectionSubmission', backref='student', lazy=True)


class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    course_code = db.Column(db.String(100))
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), default='active')  # 'active', 'archived'
    framework = db.Column(db.String(100))  # 'Bloom's Taxonomy', '5 WHYs', '1-H', 'Other'
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    reflection_due_days = db.Column(db.Integer)
    recurrence_days = db.Column(db.Integer)
    selected_days = db.Column(db.String(255))  # Comma-separated days
    custom_structure = db.Column(db.Text)  # JSON string for custom reflection structure
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade='all, delete-orphan')
    reflections = db.relationship('Reflection', backref='course', lazy=True, cascade='all, delete-orphan')


class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='unique_enrollment'),)


class Reflection(db.Model):
    __tablename__ = 'reflections'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    number = db.Column(db.Integer)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    structure = db.Column(db.Text)  # JSON string for reflection structure
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    submissions = db.relationship('ReflectionSubmission', backref='reflection', lazy=True, cascade='all, delete-orphan')


class ReflectionSubmission(db.Model):
    __tablename__ = 'reflection_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    reflection_id = db.Column(db.Integer, db.ForeignKey('reflections.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)  # JSON string for submission content
    ai_feedback = db.Column(db.Text)
    score = db.Column(db.Float)
    display_feedback = db.Column(db.Boolean, default=False)
    submitted_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('reflection_id', 'student_id', name='unique_submission'),)
