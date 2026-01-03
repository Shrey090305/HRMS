"""
DayFlow HRMS - Setup Verification Script
Checks if all required files and dependencies are in place
"""

import os
import sys

def check_file(filepath, description):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {filepath}")
    return exists

def check_directory(dirpath, description):
    """Check if a directory exists"""
    exists = os.path.isdir(dirpath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {dirpath}")
    return exists

def check_module(module_name):
    """Check if a Python module is installed"""
    try:
        __import__(module_name)
        print(f"✓ {module_name} is installed")
        return True
    except ImportError:
        print(f"✗ {module_name} is NOT installed")
        return False

def main():
    print("="*60)
    print("DayFlow HRMS - Setup Verification")
    print("="*60)
    print()
    
    all_good = True
    
    # Check core files
    print("Checking Core Files...")
    print("-"*60)
    files = [
        ('config.py', 'Configuration file'),
        ('run.py', 'Application entry point'),
        ('requirements.txt', 'Dependencies list'),
        ('init_db.py', 'Database initializer'),
        ('app/__init__.py', 'App initializer'),
        ('app/models.py', 'Database models'),
    ]
    
    for filepath, desc in files:
        if not check_file(filepath, desc):
            all_good = False
    
    print()
    
    # Check routes
    print("Checking Routes...")
    print("-"*60)
    routes = [
        'app/routes/auth.py',
        'app/routes/admin.py',
        'app/routes/employee.py',
        'app/routes/attendance.py',
        'app/routes/leave.py',
        'app/routes/payroll.py',
        'app/routes/reports.py',
    ]
    
    for route in routes:
        if not check_file(route, os.path.basename(route)):
            all_good = False
    
    print()
    
    # Check directories
    print("Checking Directories...")
    print("-"*60)
    directories = [
        'app/templates',
        'app/templates/auth',
        'app/templates/employee',
        'app/templates/admin',
        'app/templates/attendance',
        'app/templates/leave',
        'app/templates/payroll',
        'app/templates/reports',
        'app/static',
        'app/static/css',
        'app/static/js',
        'app/static/uploads/profiles',
    ]
    
    for directory in directories:
        if not check_directory(directory, os.path.basename(directory)):
            all_good = False
    
    print()
    
    # Check key templates
    print("Checking Key Templates...")
    print("-"*60)
    templates = [
        'app/templates/base.html',
        'app/templates/auth/signin.html',
        'app/templates/auth/signup.html',
        'app/templates/employee/dashboard.html',
        'app/templates/admin/dashboard.html',
    ]
    
    for template in templates:
        if not check_file(template, os.path.basename(template)):
            all_good = False
    
    print()
    
    # Check static files
    print("Checking Static Files...")
    print("-"*60)
    static_files = [
        ('app/static/css/style.css', 'Custom CSS'),
        ('app/static/js/script.js', 'Custom JavaScript'),
    ]
    
    for filepath, desc in static_files:
        if not check_file(filepath, desc):
            all_good = False
    
    print()
    
    # Check Python dependencies (only if in virtual environment or have packages)
    print("Checking Python Dependencies...")
    print("-"*60)
    modules = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_bcrypt',
        'pymysql',
    ]
    
    dependencies_ok = True
    for module in modules:
        if not check_module(module):
            dependencies_ok = False
    
    if not dependencies_ok:
        print("\n⚠ Some dependencies are missing.")
        print("Run: pip install -r requirements.txt")
        all_good = False
    
    print()
    print("="*60)
    
    if all_good:
        print("✅ All checks passed! Your setup is complete.")
        print()
        print("Next steps:")
        print("1. Create MySQL database: dayflow_hrms")
        print("2. Update config.py with your MySQL credentials")
        print("3. Run: python init_db.py")
        print("4. Run: python run.py")
        print("5. Open: http://localhost:5000")
    else:
        print("❌ Some checks failed. Please review the errors above.")
        print()
        print("Common fixes:")
        print("- Run setup.bat (Windows) to install dependencies")
        print("- Run create_dirs.py to create missing directories")
        print("- Check if all files were extracted properly")
    
    print("="*60)
    
    return all_good

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
