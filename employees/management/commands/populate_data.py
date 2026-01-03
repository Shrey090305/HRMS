from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta, datetime, time
from accounts.models import User
from employees.models import Employee
from attendance.models import Attendance
from leave.models import LeaveRequest
from payroll.models import Payroll
import random


class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data population...')
        
        # Sample data
        employees_data = [
            {'username': 'john.doe', 'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@dayflow.com',
             'employee_id': 'EMP001', 'department': 'IT', 'designation': 'Senior Developer', 'salary': 85000},
            {'username': 'jane.smith', 'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane.smith@dayflow.com',
             'employee_id': 'EMP002', 'department': 'HR', 'designation': 'HR Manager', 'salary': 75000},
            {'username': 'mike.johnson', 'first_name': 'Mike', 'last_name': 'Johnson', 'email': 'mike.j@dayflow.com',
             'employee_id': 'EMP003', 'department': 'Finance', 'designation': 'Financial Analyst', 'salary': 70000},
            {'username': 'sarah.wilson', 'first_name': 'Sarah', 'last_name': 'Wilson', 'email': 'sarah.w@dayflow.com',
             'employee_id': 'EMP004', 'department': 'IT', 'designation': 'DevOps Engineer', 'salary': 80000},
            {'username': 'david.brown', 'first_name': 'David', 'last_name': 'Brown', 'email': 'david.b@dayflow.com',
             'employee_id': 'EMP005', 'department': 'Sales', 'designation': 'Sales Executive', 'salary': 65000},
            {'username': 'emily.davis', 'first_name': 'Emily', 'last_name': 'Davis', 'email': 'emily.d@dayflow.com',
             'employee_id': 'EMP006', 'department': 'Marketing', 'designation': 'Marketing Manager', 'salary': 72000},
            {'username': 'robert.miller', 'first_name': 'Robert', 'last_name': 'Miller', 'email': 'robert.m@dayflow.com',
             'employee_id': 'EMP007', 'department': 'IT', 'designation': 'QA Engineer', 'salary': 68000},
            {'username': 'lisa.garcia', 'first_name': 'Lisa', 'last_name': 'Garcia', 'email': 'lisa.g@dayflow.com',
             'employee_id': 'EMP008', 'department': 'Operations', 'designation': 'Operations Manager', 'salary': 78000},
        ]
        
        created_employees = []
        
        # Create employees
        for emp_data in employees_data:
            if not User.objects.filter(username=emp_data['username']).exists():
                user = User.objects.create_user(
                    username=emp_data['username'],
                    email=emp_data['email'],
                    password='employee123',
                    first_name=emp_data['first_name'],
                    last_name=emp_data['last_name'],
                    role='employee'
                )
                
                employee = Employee.objects.create(
                    user=user,
                    employee_id=emp_data['employee_id'],
                    department=emp_data['department'],
                    designation=emp_data['designation'],
                    employment_type='full-time',
                    date_of_joining=date.today() - timedelta(days=random.randint(180, 730)),
                    salary=emp_data['salary'],
                    emergency_contact_name=f"{emp_data['first_name']}'s Contact",
                    emergency_contact_number=f"+91-98765{random.randint(10000, 99999)}"
                )
                created_employees.append(employee)
                self.stdout.write(self.style.SUCCESS(f'Created employee: {employee.user.get_full_name()}'))
        
        if not created_employees:
            created_employees = list(Employee.objects.all()[:8])
        
        # Create attendance records for the last 30 days
        today = date.today()
        for emp in created_employees:
            for i in range(30):
                att_date = today - timedelta(days=i)
                if att_date.weekday() < 5:  # Weekdays only
                    if not Attendance.objects.filter(employee=emp, date=att_date).exists():
                        status_choice = random.choices(
                            ['present', 'absent', 'half-day', 'on-leave'],
                            weights=[85, 5, 5, 5]
                        )[0]
                        
                        check_in = time(9, random.randint(0, 30))
                        check_out = time(17 + random.randint(0, 2), random.randint(0, 59))
                        
                        Attendance.objects.create(
                            employee=emp,
                            date=att_date,
                            check_in_time=check_in if status_choice == 'present' else None,
                            check_out_time=check_out if status_choice == 'present' else None,
                            status=status_choice
                        )
        
        self.stdout.write(self.style.SUCCESS('Created attendance records'))
        
        # Create leave requests
        leave_types = ['sick', 'casual', 'annual']
        for emp in created_employees[:5]:
            for _ in range(random.randint(2, 4)):
                start = today - timedelta(days=random.randint(10, 60))
                end = start + timedelta(days=random.randint(1, 5))
                
                if not LeaveRequest.objects.filter(employee=emp, start_date=start).exists():
                    status = random.choice(['pending', 'approved', 'approved', 'rejected'])
                    LeaveRequest.objects.create(
                        employee=emp,
                        leave_type=random.choice(leave_types),
                        start_date=start,
                        end_date=end,
                        reason=f"Personal {random.choice(['work', 'family event', 'medical appointment'])}",
                        status=status,
                        admin_remarks='Approved' if status == 'approved' else ''
                    )
        
        self.stdout.write(self.style.SUCCESS('Created leave requests'))
        
        # Create payroll records for last 3 months
        for emp in created_employees:
            for month_offset in range(3):
                payroll_date = today.replace(day=1) - timedelta(days=month_offset * 30)
                month = payroll_date.month
                year = payroll_date.year
                
                if not Payroll.objects.filter(employee=emp, month=month, year=year).exists():
                    base_salary = float(emp.salary)
                    allowances = base_salary * 0.15
                    deductions = base_salary * 0.10
                    
                    Payroll.objects.create(
                        employee=emp,
                        month=month,
                        year=year,
                        basic_salary=base_salary,
                        allowances=allowances,
                        deductions=deductions,
                        bonus=0,
                        overtime_pay=0,
                        net_salary=base_salary + allowances - deductions,
                        is_paid=month_offset > 0,
                        payment_date=payroll_date + timedelta(days=25) if month_offset > 0 else None
                    )
        
        self.stdout.write(self.style.SUCCESS('Created payroll records'))
        
        self.stdout.write(self.style.SUCCESS('✅ Data population completed!'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(created_employees)} employees'))
        self.stdout.write(self.style.WARNING('\nDefault password for all employees: employee123'))
