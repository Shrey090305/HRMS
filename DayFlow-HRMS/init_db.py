"""
Database initialization script for DayFlow HRMS
Creates all tables and inserts sample data
"""

from datetime import datetime, date, timedelta
from app import create_app, db, bcrypt
from app.models import User, Attendance, Leave, Payroll

def init_database():
    """Initialize database with tables and sample data"""
    app = create_app()
    
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        
        print("Creating all tables...")
        db.create_all()
        
        print("Creating sample data...")
        
        # Create admin user
        admin_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(
            employee_id='EMP001',
            email='admin@dayflow.com',
            password=admin_password,
            role='admin',
            first_name='John',
            last_name='Admin',
            phone='+1234567890',
            address='123 Admin Street, New York, NY',
            date_of_birth=date(1985, 5, 15),
            gender='Male',
            department='Management',
            designation='System Administrator',
            joining_date=date(2020, 1, 1),
            employment_type='Full-time',
            is_active=True
        )
        db.session.add(admin)
        
        # Create sample employees
        employees_data = [
            {
                'employee_id': 'EMP002',
                'email': 'alice@dayflow.com',
                'first_name': 'Alice',
                'last_name': 'Smith',
                'department': 'Engineering',
                'designation': 'Senior Developer',
                'phone': '+1234567891'
            },
            {
                'employee_id': 'EMP003',
                'email': 'bob@dayflow.com',
                'first_name': 'Bob',
                'last_name': 'Johnson',
                'department': 'Engineering',
                'designation': 'Junior Developer',
                'phone': '+1234567892'
            },
            {
                'employee_id': 'EMP004',
                'email': 'carol@dayflow.com',
                'first_name': 'Carol',
                'last_name': 'Williams',
                'department': 'HR',
                'designation': 'HR Manager',
                'phone': '+1234567893'
            },
            {
                'employee_id': 'EMP005',
                'email': 'david@dayflow.com',
                'first_name': 'David',
                'last_name': 'Brown',
                'department': 'Sales',
                'designation': 'Sales Executive',
                'phone': '+1234567894'
            },
            {
                'employee_id': 'EMP006',
                'email': 'emma@dayflow.com',
                'first_name': 'Emma',
                'last_name': 'Davis',
                'department': 'Marketing',
                'designation': 'Marketing Manager',
                'phone': '+1234567895'
            }
        ]
        
        employee_password = bcrypt.generate_password_hash('employee123').decode('utf-8')
        employees = []
        
        for emp_data in employees_data:
            employee = User(
                employee_id=emp_data['employee_id'],
                email=emp_data['email'],
                password=employee_password,
                role='employee',
                first_name=emp_data['first_name'],
                last_name=emp_data['last_name'],
                phone=emp_data['phone'],
                address=f"456 Employee Lane, City, State",
                date_of_birth=date(1990, 1, 1),
                gender='Male' if emp_data['first_name'] in ['Bob', 'David'] else 'Female',
                department=emp_data['department'],
                designation=emp_data['designation'],
                joining_date=date(2021, 6, 1),
                employment_type='Full-time',
                is_active=True
            )
            db.session.add(employee)
            employees.append(employee)
        
        db.session.commit()
        print(f"Created {len(employees) + 1} users (1 admin, {len(employees)} employees)")
        
        # Create attendance records for the last 7 days
        today = date.today()
        attendance_count = 0
        
        for employee in employees:
            for i in range(7):
                attendance_date = today - timedelta(days=i)
                
                # Random attendance status
                import random
                statuses = ['Present', 'Present', 'Present', 'Absent', 'Half-day']
                status = random.choice(statuses)
                
                attendance = Attendance(
                    user_id=employee.id,
                    date=attendance_date,
                    check_in=datetime.strptime('09:00', '%H:%M').time() if status == 'Present' else None,
                    check_out=datetime.strptime('17:00', '%H:%M').time() if status == 'Present' else None,
                    status=status
                )
                db.session.add(attendance)
                attendance_count += 1
        
        db.session.commit()
        print(f"Created {attendance_count} attendance records")
        
        # Create sample leave requests
        leave_types = ['Sick', 'Casual', 'Annual', 'Emergency']
        leave_statuses = ['Pending', 'Approved', 'Rejected']
        leave_count = 0
        
        for i, employee in enumerate(employees[:3]):  # First 3 employees
            start_date = today + timedelta(days=7 + i)
            end_date = start_date + timedelta(days=2)
            
            leave = Leave(
                user_id=employee.id,
                leave_type=leave_types[i % len(leave_types)],
                start_date=start_date,
                end_date=end_date,
                days=3,
                reason=f"Sample leave request for {leave_types[i % len(leave_types)]} leave",
                status=leave_statuses[i % len(leave_statuses)],
                applied_at=datetime.utcnow() - timedelta(days=i)
            )
            db.session.add(leave)
            leave_count += 1
        
        db.session.commit()
        print(f"Created {leave_count} leave requests")
        
        # Create payroll records
        months = ['December', 'November', 'October']
        payroll_count = 0
        
        for employee in employees:
            for i, month in enumerate(months):
                payroll = Payroll(
                    user_id=employee.id,
                    month=month,
                    year=2025 if month == 'December' else 2026,
                    basic_salary=5000.00 + (i * 100),
                    allowances=500.00,
                    deductions=300.00,
                    net_salary=5200.00 + (i * 100),
                    payment_status='Paid' if i > 0 else 'Pending',
                    payment_date=date(2025 if month == 'December' else 2026, 12 - i, 25) if i > 0 else None
                )
                db.session.add(payroll)
                payroll_count += 1
        
        db.session.commit()
        print(f"Created {payroll_count} payroll records")
        
        print("\n" + "="*50)
        print("Database initialized successfully!")
        print("="*50)
        print("\nLogin Credentials:")
        print("-" * 50)
        print("Admin:")
        print("  Email: admin@dayflow.com")
        print("  Password: admin123")
        print("\nEmployee (any of the following):")
        print("  Email: alice@dayflow.com, bob@dayflow.com, etc.")
        print("  Password: employee123")
        print("="*50)

if __name__ == '__main__':
    init_database()
