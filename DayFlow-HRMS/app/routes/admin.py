from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db, bcrypt
from app.models import User, Attendance, Leave, Payroll
from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy import func
import os
from werkzeug.utils import secure_filename

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied! Admin access only.', 'danger')
            return redirect(url_for('auth.signin'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get statistics
    total_employees = User.query.filter_by(role='employee', is_active=True).count()
    
    today = datetime.utcnow().date()
    present_today = Attendance.query.filter_by(date=today, status='Present').count()
    
    pending_leaves = Leave.query.filter_by(status='Pending').count()
    
    # Recent employees
    recent_employees = User.query.filter_by(role='employee').order_by(User.created_at.desc()).limit(5).all()
    
    # Recent leave requests
    recent_leaves = Leave.query.order_by(Leave.applied_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_employees=total_employees,
                         present_today=present_today,
                         pending_leaves=pending_leaves,
                         recent_employees=recent_employees,
                         recent_leaves=recent_leaves)

@admin.route('/employees')
@login_required
@admin_required
def employees():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = User.query.filter_by(role='employee')
    
    if search:
        query = query.filter(
            (User.employee_id.like(f'%{search}%')) |
            (User.email.like(f'%{search}%')) |
            (User.first_name.like(f'%{search}%')) |
            (User.last_name.like(f'%{search}%'))
        )
    
    employees = query.order_by(User.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    
    return render_template('admin/employees.html', employees=employees, search=search)

@admin.route('/employee/<int:user_id>')
@login_required
@admin_required
def employee_detail(user_id):
    user = User.query.get_or_404(user_id)
    if user.role != 'employee':
        flash('Invalid employee!', 'danger')
        return redirect(url_for('admin.employees'))
    
    return render_template('admin/employee_detail.html', user=user)

@admin.route('/employee/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_employee(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.phone = request.form.get('phone')
        user.address = request.form.get('address')
        
        # Date fields
        dob = request.form.get('date_of_birth')
        if dob:
            user.date_of_birth = datetime.strptime(dob, '%Y-%m-%d').date()
        
        user.gender = request.form.get('gender')
        user.department = request.form.get('department')
        user.designation = request.form.get('designation')
        
        joining = request.form.get('joining_date')
        if joining:
            user.joining_date = datetime.strptime(joining, '%Y-%m-%d').date()
        
        user.employment_type = request.form.get('employment_type')
        user.is_active = request.form.get('is_active') == 'on'
        
        # Handle profile picture upload
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename:
                filename = secure_filename(f"{user.employee_id}_{file.filename}")
                filepath = os.path.join('app', 'static', 'uploads', 'profiles', filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                file.save(filepath)
                user.profile_picture = f'profiles/{filename}'
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('admin.employee_detail', user_id=user.id))
    
    return render_template('admin/edit_employee.html', user=user)

@admin.route('/employee/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_employee():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user already exists
        existing_user = User.query.filter(
            (User.employee_id == employee_id) | (User.email == email)
        ).first()
        
        if existing_user:
            flash('Employee ID or Email already exists!', 'danger')
            return render_template('admin/add_employee.html')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            employee_id=employee_id,
            email=email,
            password=hashed_password,
            role='employee',
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            phone=request.form.get('phone'),
            department=request.form.get('department'),
            designation=request.form.get('designation')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Employee added successfully!', 'success')
        return redirect(url_for('admin.employees'))
    
    return render_template('admin/add_employee.html')
