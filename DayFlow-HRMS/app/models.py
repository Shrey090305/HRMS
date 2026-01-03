from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='employee')  # employee or admin
    
    # Personal Information
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    address = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    profile_picture = db.Column(db.String(255), default='default.jpg')
    
    # Job Information
    department = db.Column(db.String(100))
    designation = db.Column(db.String(100))
    joining_date = db.Column(db.Date)
    employment_type = db.Column(db.String(50))  # Full-time, Part-time, Contract
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendance_records = db.relationship('Attendance', backref='employee', lazy=True, cascade='all, delete-orphan')
    leave_requests = db.relationship('Leave', backref='employee', lazy=True, cascade='all, delete-orphan')
    payroll_records = db.relationship('Payroll', backref='employee', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.employee_id} - {self.email}>'
    
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.employee_id


class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.Time)
    check_out = db.Column(db.Time)
    status = db.Column(db.String(20), nullable=False)  # Present, Absent, Half-day, Leave
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Attendance {self.employee.employee_id} - {self.date} - {self.status}>'


class Leave(db.Model):
    __tablename__ = 'leaves'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)  # Sick, Casual, Annual, Emergency
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')  # Pending, Approved, Rejected
    admin_comments = db.Column(db.Text)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Leave {self.employee.employee_id} - {self.leave_type} - {self.status}>'


class Payroll(db.Model):
    __tablename__ = 'payroll'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    month = db.Column(db.String(20), nullable=False)  # e.g., "January 2026"
    year = db.Column(db.Integer, nullable=False)
    basic_salary = db.Column(db.Float, nullable=False)
    allowances = db.Column(db.Float, default=0.0)
    deductions = db.Column(db.Float, default=0.0)
    net_salary = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date)
    payment_status = db.Column(db.String(20), default='Pending')  # Pending, Paid
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Payroll {self.employee.employee_id} - {self.month} {self.year}>'
