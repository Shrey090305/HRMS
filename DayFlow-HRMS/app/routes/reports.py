from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Attendance, Leave, User
from datetime import datetime, timedelta
from sqlalchemy import func, and_

reports = Blueprint('reports', __name__, url_prefix='/reports')

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied! Admin access only.', 'danger')
            return redirect(url_for('auth.signin'))
        return f(*args, **kwargs)
    return decorated_function

@reports.route('/')
@login_required
@admin_required
def index():
    return render_template('reports/index.html')

@reports.route('/attendance')
@login_required
@admin_required
def attendance_report():
    # Get date range from query params or default to last 30 days
    end_date = request.args.get('end_date', datetime.utcnow().date().strftime('%Y-%m-%d'))
    end = datetime.strptime(end_date, '%Y-%m-%d').date()
    start = end - timedelta(days=29)
    start_date = request.args.get('start_date', start.strftime('%Y-%m-%d'))
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    
    # Get attendance records for date range
    records = db.session.query(
        User.employee_id,
        User.first_name,
        User.last_name,
        func.count(Attendance.id).label('total_days'),
        func.sum(func.case((Attendance.status == 'Present', 1), else_=0)).label('present'),
        func.sum(func.case((Attendance.status == 'Absent', 1), else_=0)).label('absent'),
        func.sum(func.case((Attendance.status == 'Half-day', 1), else_=0)).label('half_day'),
        func.sum(func.case((Attendance.status == 'Leave', 1), else_=0)).label('on_leave')
    ).join(Attendance).filter(
        and_(
            Attendance.date >= start,
            Attendance.date <= end,
            User.role == 'employee'
        )
    ).group_by(User.id).all()
    
    return render_template('reports/attendance_report.html',
                         records=records,
                         start_date=start,
                         end_date=end)

@reports.route('/leave')
@login_required
@admin_required
def leave_report():
    year = request.args.get('year', datetime.utcnow().year, type=int)
    
    # Get leave summary by employee
    records = db.session.query(
        User.employee_id,
        User.first_name,
        User.last_name,
        func.count(Leave.id).label('total_requests'),
        func.sum(func.case((Leave.status == 'Approved', Leave.days), else_=0)).label('approved_days'),
        func.sum(func.case((Leave.status == 'Pending', 1), else_=0)).label('pending_requests'),
        func.sum(func.case((Leave.status == 'Rejected', 1), else_=0)).label('rejected_requests')
    ).join(Leave).filter(
        and_(
            func.extract('year', Leave.start_date) == year,
            User.role == 'employee'
        )
    ).group_by(User.id).all()
    
    return render_template('reports/leave_report.html', records=records, year=year)

@reports.route('/api/attendance-chart')
@login_required
@admin_required
def attendance_chart():
    # Get last 7 days data
    today = datetime.utcnow().date()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    
    data = {
        'dates': dates,
        'present': [],
        'absent': [],
        'half_day': [],
        'leave': []
    }
    
    for date_str in dates:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        present = Attendance.query.filter_by(date=date, status='Present').count()
        absent = Attendance.query.filter_by(date=date, status='Absent').count()
        half_day = Attendance.query.filter_by(date=date, status='Half-day').count()
        leave = Attendance.query.filter_by(date=date, status='Leave').count()
        
        data['present'].append(present)
        data['absent'].append(absent)
        data['half_day'].append(half_day)
        data['leave'].append(leave)
    
    return jsonify(data)

@reports.route('/api/leave-chart')
@login_required
@admin_required
def leave_chart():
    year = request.args.get('year', datetime.utcnow().year, type=int)
    
    # Get leave counts by type
    leave_types = ['Sick', 'Casual', 'Annual', 'Emergency']
    data = {
        'types': leave_types,
        'counts': []
    }
    
    for leave_type in leave_types:
        count = Leave.query.filter(
            and_(
                Leave.leave_type == leave_type,
                Leave.status == 'Approved',
                func.extract('year', Leave.start_date) == year
            )
        ).count()
        data['counts'].append(count)
    
    return jsonify(data)
