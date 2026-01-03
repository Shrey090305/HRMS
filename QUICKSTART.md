# DayFlow HRMS - Quick Start Guide

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install PostgreSQL
1. Download PostgreSQL from https://www.postgresql.org/download/
2. Install with default settings
3. Remember your PostgreSQL password

### Step 2: Create Database
Open PostgreSQL terminal (psql) or pgAdmin and run:
```sql
CREATE DATABASE dayflow_hrms;
```

### Step 3: Setup Python Environment
```bash
# Navigate to project directory
cd c:\Users\Shrey\Desktop\DayFlow-HRMS

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Database
Edit `dayflow/settings.py` line 76-82:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dayflow_hrms',
        'USER': 'postgres',
        'PASSWORD': 'YOUR_POSTGRESQL_PASSWORD',  # ← Change this
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Step 5: Initialize Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Admin User
```bash
python manage.py createsuperuser
```
Enter:
- Username: `admin`
- Email: `admin@dayflow.com`
- Password: (your choice)

### Step 7: Run Server
```bash
python manage.py runserver
```

### Step 8: Access Application
Open browser: http://localhost:8000

---

## 🎯 First Login

### Admin Login
1. Go to http://localhost:8000
2. Login with superuser credentials
3. You'll be redirected to Admin Dashboard

### Create First Employee
1. Click "Add Employee" button
2. Fill in employee details
3. Create user credentials
4. Save

---

## 📋 Common Tasks

### Mark Attendance (Employee)
1. Login as employee
2. Click "Mark Attendance"
3. Click "Check In"
4. At end of day, click "Check Out"

### Apply for Leave (Employee)
1. Go to "Leave" section
2. Click "Apply Leave"
3. Select leave type and dates
4. Submit request

### Approve Leave (Admin)
1. Go to "Leave Management"
2. View pending requests
3. Click "Approve" or "Reject"

### Add Payroll (Admin)
1. Go to "Payroll"
2. Click "Add Payroll"
3. Select employee and month
4. Enter salary components
5. Save

---

## 🔧 Troubleshooting

### Database Connection Error
- Verify PostgreSQL is running
- Check database name and credentials in `settings.py`
- Test connection: `psql -U postgres -d dayflow_hrms`

### Module Not Found Error
```bash
pip install -r requirements.txt
```

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

---

## 📱 Test Accounts

After setup, create test accounts:

### Admin Account
- Role: Admin
- Full access to all features

### Employee Account
- Role: Employee
- Limited to personal features

---

## 🎓 Next Steps

1. **Customize Settings**: Edit `settings.py` for your needs
2. **Add Employees**: Populate your employee database
3. **Configure Email**: Set up email notifications
4. **Backup Database**: Regular backups recommended

---

## 📞 Need Help?

- Check README.md for detailed documentation
- Review Django documentation: https://docs.djangoproject.com
- Check PostgreSQL docs: https://www.postgresql.org/docs/

---

**You're all set! Happy managing! 🎉**
