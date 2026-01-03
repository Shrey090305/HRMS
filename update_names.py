import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dayflow.settings')
django.setup()

from accounts.models import User
from employees.models import Employee

# Indian names to replace existing names
indian_names = [
    ('Rahul', 'Sharma'),
    ('Priya', 'Patel'),
    ('Amit', 'Kumar'),
    ('Sneha', 'Singh'),
    ('Vikram', 'Reddy'),
    ('Anjali', 'Gupta'),
    ('Rohan', 'Joshi'),
    ('Neha', 'Verma'),
]

# Get all employees
employees = Employee.objects.all().order_by('id')

print(f"Found {employees.count()} employees")

# Update each employee's name
for i, emp in enumerate(employees):
    if i < len(indian_names):
        first_name, last_name = indian_names[i]
        user = emp.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        print(f"Updated: {user.username} -> {first_name} {last_name}")
    else:
        print(f"Skipping employee {i+1} - not enough names")

print("\nAll names updated successfully!")
