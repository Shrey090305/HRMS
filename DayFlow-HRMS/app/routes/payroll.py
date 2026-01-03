from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Payroll, User
from datetime import datetime

payroll = Blueprint('payroll', __name__, url_prefix='/payroll')

@payroll.route('/')
@login_required
def index():
    if current_user.role == 'employee':
        # Employee sees only their payroll
        payrolls = Payroll.query.filter_by(user_id=current_user.id).order_by(
            Payroll.year.desc(), Payroll.month.desc()
        ).all()
        return render_template('payroll/employee_payroll.html', payrolls=payrolls)
    else:
        # Admin sees all payroll
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '')
        
        query = Payroll.query
        
        if search:
            users = User.query.filter(
                (User.employee_id.like(f'%{search}%')) |
                (User.first_name.like(f'%{search}%')) |
                (User.last_name.like(f'%{search}%'))
            ).all()
            user_ids = [u.id for u in users]
            query = query.filter(Payroll.user_id.in_(user_ids))
        
        payrolls = query.order_by(Payroll.year.desc(), Payroll.month.desc()).paginate(
            page=page, per_page=15, error_out=False
        )
        
        return render_template('payroll/admin_payroll.html', payrolls=payrolls, search=search)

@payroll.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('payroll.index'))
    
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        month = request.form.get('month')
        year = request.form.get('year')
        basic_salary = float(request.form.get('basic_salary', 0))
        allowances = float(request.form.get('allowances', 0))
        deductions = float(request.form.get('deductions', 0))
        
        net_salary = basic_salary + allowances - deductions
        
        # Check if payroll already exists
        existing = Payroll.query.filter_by(
            user_id=user_id,
            month=month,
            year=year
        ).first()
        
        if existing:
            flash('Payroll for this employee and period already exists!', 'danger')
            employees = User.query.filter_by(role='employee', is_active=True).all()
            return render_template('payroll/add_payroll.html', employees=employees)
        
        new_payroll = Payroll(
            user_id=user_id,
            month=month,
            year=year,
            basic_salary=basic_salary,
            allowances=allowances,
            deductions=deductions,
            net_salary=net_salary,
            payment_status='Pending'
        )
        
        db.session.add(new_payroll)
        db.session.commit()
        
        flash('Payroll added successfully!', 'success')
        return redirect(url_for('payroll.index'))
    
    employees = User.query.filter_by(role='employee', is_active=True).all()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    return render_template('payroll/add_payroll.html', employees=employees, months=months)

@payroll.route('/<int:payroll_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(payroll_id):
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('payroll.index'))
    
    payroll_record = Payroll.query.get_or_404(payroll_id)
    
    if request.method == 'POST':
        payroll_record.basic_salary = float(request.form.get('basic_salary', 0))
        payroll_record.allowances = float(request.form.get('allowances', 0))
        payroll_record.deductions = float(request.form.get('deductions', 0))
        payroll_record.net_salary = (payroll_record.basic_salary + 
                                     payroll_record.allowances - 
                                     payroll_record.deductions)
        payroll_record.payment_status = request.form.get('payment_status', 'Pending')
        
        payment_date = request.form.get('payment_date')
        if payment_date:
            payroll_record.payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()
        
        payroll_record.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Payroll updated successfully!', 'success')
        return redirect(url_for('payroll.index'))
    
    return render_template('payroll/edit_payroll.html', payroll=payroll_record)

@payroll.route('/<int:payroll_id>/detail')
@login_required
def detail(payroll_id):
    payroll_record = Payroll.query.get_or_404(payroll_id)
    
    # Check permission
    if current_user.role == 'employee' and payroll_record.user_id != current_user.id:
        flash('Access denied!', 'danger')
        return redirect(url_for('payroll.index'))
    
    return render_template('payroll/payroll_detail.html', payroll=payroll_record)
