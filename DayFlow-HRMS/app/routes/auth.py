from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import User
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('employee.dashboard'))
    return redirect(url_for('auth.signin'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'employee')
        
        # Validation
        if not all([employee_id, email, password, confirm_password]):
            flash('All fields are required!', 'danger')
            return render_template('auth/signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('auth/signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'danger')
            return render_template('auth/signup.html')
        
        # Check if user already exists
        existing_user = User.query.filter(
            (User.employee_id == employee_id) | (User.email == email)
        ).first()
        
        if existing_user:
            flash('Employee ID or Email already exists!', 'danger')
            return render_template('auth/signup.html')
        
        # Hash password and create user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            employee_id=employee_id,
            email=email,
            password=hashed_password,
            role=role
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please sign in.', 'success')
        return redirect(url_for('auth.signin'))
    
    return render_template('auth/signup.html')

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        if not email or not password:
            flash('Email and password are required!', 'danger')
            return render_template('auth/signin.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            if not user.is_active:
                flash('Your account has been deactivated. Contact admin.', 'danger')
                return render_template('auth/signin.html')
            
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            
            if next_page:
                return redirect(next_page)
            elif user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('employee.dashboard'))
        else:
            flash('Invalid email or password!', 'danger')
    
    return render_template('auth/signin.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('auth.signin'))
