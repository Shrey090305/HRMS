from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Attendance
from datetime import datetime, timedelta
from sqlalchemy import and_

attendance = Blueprint('attendance', __name__, url_prefix='/attendance')

@attendance.route('/')
@login_required
def index():
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=6)  # Last 7 days
    
    if current_user.role == 'employee':
        # Employee sees only their attendance
        records = Attendance.query.filter(
            and_(
                Attendance.user_id == current_user.id,
                Attendance.date >= week_ago,
                Attendance.date <= today
            )
        ).order_by(Attendance.date.desc()).all()
        
        today_record = Attendance.query.filter_by(
            user_id=current_user.id,
            date=today
        ).first()
        
        return render_template('attendance/employee_attendance.html',
                             records=records,
                             today_record=today_record,
                             today=today)
    else:
        # Admin sees all attendance
        page = request.args.get('page', 1, type=int)
        date_filter = request.args.get('date', today.strftime('%Y-%m-%d'))
        filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
        
        records = Attendance.query.filter_by(date=filter_date).order_by(Attendance.id.desc()).paginate(
            page=page, per_page=20, error_out=False
        )
        
        # Statistics for the day
        present = Attendance.query.filter_by(date=filter_date, status='Present').count()
        absent = Attendance.query.filter_by(date=filter_date, status='Absent').count()
        half_day = Attendance.query.filter_by(date=filter_date, status='Half-day').count()
        on_leave = Attendance.query.filter_by(date=filter_date, status='Leave').count()
        
        return render_template('attendance/admin_attendance.html',
                             records=records,
                             filter_date=filter_date,
                             present=present,
                             absent=absent,
                             half_day=half_day,
                             on_leave=on_leave)

@attendance.route('/checkin', methods=['POST'])
@login_required
def checkin():
    if current_user.role != 'employee':
        return jsonify({'success': False, 'message': 'Only employees can check in'}), 403
    
    today = datetime.utcnow().date()
    now = datetime.utcnow().time()
    
    # Check if already checked in today
    existing = Attendance.query.filter_by(
        user_id=current_user.id,
        date=today
    ).first()
    
    if existing:
        return jsonify({'success': False, 'message': 'Already checked in today'}), 400
    
    new_attendance = Attendance(
        user_id=current_user.id,
        date=today,
        check_in=now,
        status='Present'
    )
    
    db.session.add(new_attendance)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Checked in successfully!',
        'check_in': now.strftime('%H:%M:%S')
    })

@attendance.route('/checkout', methods=['POST'])
@login_required
def checkout():
    if current_user.role != 'employee':
        return jsonify({'success': False, 'message': 'Only employees can check out'}), 403
    
    today = datetime.utcnow().date()
    now = datetime.utcnow().time()
    
    attendance_record = Attendance.query.filter_by(
        user_id=current_user.id,
        date=today
    ).first()
    
    if not attendance_record:
        return jsonify({'success': False, 'message': 'No check-in found for today'}), 400
    
    if attendance_record.check_out:
        return jsonify({'success': False, 'message': 'Already checked out'}), 400
    
    attendance_record.check_out = now
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Checked out successfully!',
        'check_out': now.strftime('%H:%M:%S')
    })

@attendance.route('/mark/<int:user_id>', methods=['POST'])
@login_required
def mark_attendance(user_id):
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('attendance.index'))
    
    date_str = request.form.get('date')
    status = request.form.get('status')
    remarks = request.form.get('remarks', '')
    
    if not date_str or not status:
        flash('Date and status are required!', 'danger')
        return redirect(url_for('attendance.index'))
    
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Check if attendance already exists
    existing = Attendance.query.filter_by(user_id=user_id, date=date).first()
    
    if existing:
        existing.status = status
        existing.remarks = remarks
        existing.updated_at = datetime.utcnow()
    else:
        new_attendance = Attendance(
            user_id=user_id,
            date=date,
            status=status,
            remarks=remarks
        )
        db.session.add(new_attendance)
    
    db.session.commit()
    flash('Attendance marked successfully!', 'success')
    return redirect(url_for('attendance.index'))
