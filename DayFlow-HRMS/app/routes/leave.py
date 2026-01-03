from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Leave, User
from datetime import datetime

leave = Blueprint('leave', __name__, url_prefix='/leave')

@leave.route('/')
@login_required
def index():
    if current_user.role == 'employee':
        # Employee sees only their leave requests
        leaves = Leave.query.filter_by(user_id=current_user.id).order_by(Leave.applied_at.desc()).all()
        return render_template('leave/employee_leave.html', leaves=leaves)
    else:
        # Admin sees all leave requests
        status_filter = request.args.get('status', 'all')
        page = request.args.get('page', 1, type=int)
        
        query = Leave.query
        
        if status_filter != 'all':
            query = query.filter_by(status=status_filter)
        
        leaves = query.order_by(Leave.applied_at.desc()).paginate(page=page, per_page=15, error_out=False)
        
        # Statistics
        pending_count = Leave.query.filter_by(status='Pending').count()
        approved_count = Leave.query.filter_by(status='Approved').count()
        rejected_count = Leave.query.filter_by(status='Rejected').count()
        
        return render_template('leave/admin_leave.html',
                             leaves=leaves,
                             status_filter=status_filter,
                             pending_count=pending_count,
                             approved_count=approved_count,
                             rejected_count=rejected_count)

@leave.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
    if current_user.role != 'employee':
        flash('Only employees can apply for leave!', 'danger')
        return redirect(url_for('leave.index'))
    
    if request.method == 'POST':
        leave_type = request.form.get('leave_type')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        reason = request.form.get('reason')
        
        if not all([leave_type, start_date, end_date, reason]):
            flash('All fields are required!', 'danger')
            return render_template('leave/apply_leave.html')
        
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        if end < start:
            flash('End date cannot be before start date!', 'danger')
            return render_template('leave/apply_leave.html')
        
        days = (end - start).days + 1
        
        new_leave = Leave(
            user_id=current_user.id,
            leave_type=leave_type,
            start_date=start,
            end_date=end,
            days=days,
            reason=reason,
            status='Pending'
        )
        
        db.session.add(new_leave)
        db.session.commit()
        
        flash('Leave request submitted successfully!', 'success')
        return redirect(url_for('leave.index'))
    
    return render_template('leave/apply_leave.html')

@leave.route('/<int:leave_id>/detail')
@login_required
def detail(leave_id):
    leave_request = Leave.query.get_or_404(leave_id)
    
    # Check permission
    if current_user.role == 'employee' and leave_request.user_id != current_user.id:
        flash('Access denied!', 'danger')
        return redirect(url_for('leave.index'))
    
    return render_template('leave/leave_detail.html', leave=leave_request)

@leave.route('/<int:leave_id>/review', methods=['POST'])
@login_required
def review(leave_id):
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('leave.index'))
    
    leave_request = Leave.query.get_or_404(leave_id)
    
    action = request.form.get('action')
    comments = request.form.get('comments', '')
    
    if action not in ['Approved', 'Rejected']:
        flash('Invalid action!', 'danger')
        return redirect(url_for('leave.detail', leave_id=leave_id))
    
    leave_request.status = action
    leave_request.admin_comments = comments
    leave_request.reviewed_at = datetime.utcnow()
    
    db.session.commit()
    
    flash(f'Leave request {action.lower()} successfully!', 'success')
    return redirect(url_for('leave.index'))
