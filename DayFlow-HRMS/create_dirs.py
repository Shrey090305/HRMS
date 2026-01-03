"""
Create necessary directories for DayFlow HRMS
"""
import os

def create_directories():
    """Create all required directories"""
    directories = [
        'app/static/uploads/profiles',
        'app/static/css',
        'app/static/js',
        'app/templates/auth',
        'app/templates/employee',
        'app/templates/admin',
        'app/templates/attendance',
        'app/templates/leave',
        'app/templates/payroll',
        'app/templates/reports',
        'app/routes'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created/verified: {directory}")
    
    print("\n✅ All directories created successfully!")

if __name__ == '__main__':
    create_directories()
