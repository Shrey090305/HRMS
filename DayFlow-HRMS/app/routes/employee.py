from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db, bcrypt
from app.models import User, Attendance, Leave, Payroll
from datetime import datetime, timedelta
from functools import wraps
import os
from werkzeug.utils import secure_filename

employee = Blueprint('employee', __name__, url_prefix='/employee')

def employee_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'employee':
            flash('Access denied! Employee access only.', 'danger')
            return redirect(url_for('auth.signin'))
        return f(*args, **kwargs)
    return decorated_function

@employee.route('/dashboard')
@login_required
@employee_required
def dashboard():
    # Get today's attendance
    today = datetime.utcnow().date()
    today_attendance = Attendance.query.filter_by(
        user_id=current_user.id,
        date=today
    ).first()
    
    # Get recent attendance (last 7 days)
    week_ago = today - timedelta(days=7)
    recent_attendance = Attendance.query.filter(
        Attendance.user_id == current_user.id,
        Attendance.date >= week_ago
    ).order_by(Attendance.date.desc()).all()
    
    # Get pending leave requests
    pending_leaves = Leave.query.filter_by(
        user_id=current_user.id,
        status='Pending'
    ).count()
    
    # Get latest payroll
    latest_payroll = Payroll.query.filter_by(
        user_id=current_user.id
    ).order_by(Payroll.year.desc(), Payroll.month.desc()).first()
    
    return render_template('employee/dashboard.html',
                         today_attendance=today_attendance,
                         recent_attendance=recent_attendance,
                         pending_leaves=pending_leaves,
                         latest_payroll=latest_payroll)

@employee.route('/profile')
@login_required
@employee_required
def profile():
    return render_template('employee/profile.html', user=current_user)

@employee.route('/profile/edit', methods=['GET', 'POST'])
@login_required
@employee_required
def edit_profile():
    if request.method == 'POST':
        # Employee can edit limited fields
        current_user.phone = request.form.get('phone')
        current_user.address = request.form.get('address')
        
        # Handle profile picture upload
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename:
                filename = secure_filename(f"{current_user.employee_id}_{file.filename}")
                filepath = os.path.join('app', 'static', 'uploads', 'profiles', filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                file.save(filepath)
                current_user.profile_picture = f'profiles/{filename}'
        
        current_user.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('employee.profile'))
    
    return render_template('employee/edit_profile.html', user=current_user)
