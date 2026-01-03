# DayFlow HRMS - Django + PostgreSQL

A comprehensive Human Resource Management System built with Django and PostgreSQL.

## 🚀 Features

- **User Authentication**: Role-based access (Admin/Employee)
- **Employee Management**: Complete CRUD operations for employee records
- **Attendance Tracking**: Daily check-in/check-out with working hours calculation
- **Leave Management**: Leave requests with approval workflow
- **Payroll System**: Salary management with allowances and deductions
- **Reports & Analytics**: Comprehensive reports for all modules

## 🛠 Tech Stack

### Backend
- **Django 5.0** - Web framework
- **PostgreSQL** - Database
- **Django ORM** - Database abstraction

### Frontend
- **Bootstrap 5** - UI framework
- **jQuery** - JavaScript library
- **Font Awesome** - Icons

## 📋 Prerequisites

- Python 3.10 or higher
- PostgreSQL 14 or higher
- pip (Python package manager)

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
cd c:\Users\Shrey\Desktop\DayFlow-HRMS
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure PostgreSQL Database

**Create Database:**
```sql
-- Open PostgreSQL command line or pgAdmin
CREATE DATABASE dayflow_hrms;
CREATE USER postgres WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE dayflow_hrms TO postgres;
```

**Update Settings:**
Edit `dayflow/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dayflow_hrms',
        'USER': 'postgres',
        'PASSWORD': 'your_password',  # Change this
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 8. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 9. Run Development Server
```bash
python manage.py runserver
```

Visit: http://localhost:8000

## 📁 Project Structure

```
DayFlow-HRMS/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── dayflow/                  # Project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI config
│   └── asgi.py              # ASGI config
├── accounts/                 # Authentication app
│   ├── models.py            # User model
│   ├── views.py             # Auth views
│   ├── forms.py             # Auth forms
│   └── urls.py              # Auth URLs
├── employees/                # Employee management
│   ├── models.py            # Employee model
│   ├── views.py             # Employee views
│   ├── forms.py             # Employee forms
│   └── urls.py              # Employee URLs
├── attendance/               # Attendance tracking
│   ├── models.py            # Attendance model
│   ├── views.py             # Attendance views
│   └── urls.py              # Attendance URLs
├── leave/                    # Leave management
│   ├── models.py            # Leave request model
│   ├── views.py             # Leave views
│   └── urls.py              # Leave URLs
├── payroll/                  # Payroll system
│   ├── models.py            # Payroll models
│   ├── views.py             # Payroll views
│   └── urls.py              # Payroll URLs
├── reports/                  # Reports & analytics
│   ├── views.py             # Report views
│   └── urls.py              # Report URLs
├── templates/                # HTML templates
│   ├── base.html            # Base template
│   ├── accounts/            # Auth templates
│   ├── employees/           # Employee templates
│   ├── attendance/          # Attendance templates
│   ├── leave/               # Leave templates
│   └── payroll/             # Payroll templates
└── static/                   # Static files
    ├── css/                 # Stylesheets
    └── js/                  # JavaScript files
```

## 👥 User Roles

### Admin
- Manage all employees
- View and approve leave requests
- Manage attendance records
- Process payroll
- Generate reports

### Employee
- View personal profile
- Mark daily attendance
- Apply for leaves
- View payroll records
- View leave history

## 🔐 Default Admin Credentials

After creating superuser, you can login with your credentials.

To create an admin user programmatically:
```python
python manage.py shell
from accounts.models import User
user = User.objects.create_superuser(
    username='admin',
    email='admin@dayflow.com',
    password='admin123',
    role='admin',
    first_name='Admin',
    last_name='User'
)
```

## 📊 Database Schema

### Key Models:

- **User**: Custom user model with role-based access
- **Employee**: Extended employee information
- **Attendance**: Daily attendance records
- **LeaveRequest**: Leave management
- **Payroll**: Salary and payment records

## 🎯 Key Features

### 1. Attendance System
- Quick check-in/check-out
- Working hours calculation
- Attendance history
- Admin oversight

### 2. Leave Management
- Multiple leave types (Sick, Casual, Annual, etc.)
- Approval workflow
- Leave balance tracking
- Email notifications

### 3. Payroll Processing
- Salary components (Basic, Allowances, Deductions)
- Monthly payroll generation
- Payment tracking
- Payslip generation

### 4. Reports & Analytics
- Attendance reports
- Leave statistics
- Payroll summaries
- Department-wise analytics

## 🔧 Environment Variables (Optional)

Create a `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_NAME=dayflow_hrms
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

Install python-decouple:
```bash
pip install python-decouple
```

## 🚀 Production Deployment

### 1. Update Settings
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SECRET_KEY = 'production-secret-key'
```

### 2. Use Production Database
Configure PostgreSQL for production use.

### 3. Serve Static Files
```bash
python manage.py collectstatic
```

### 4. Use Gunicorn
```bash
pip install gunicorn
gunicorn dayflow.wsgi:application
```

## 🧪 Running Tests
```bash
python manage.py test
```

## 📝 API Endpoints (Optional)

If using Django REST Framework:
- `/api/employees/` - Employee list/create
- `/api/attendance/` - Attendance records
- `/api/leave/` - Leave requests
- `/api/payroll/` - Payroll records

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is proprietary software for DayFlow HRMS.

## 📧 Support

For support, email: support@dayflow.com

## 🔄 Updates & Maintenance

Regular updates include:
- Security patches
- Feature enhancements
- Bug fixes
- Performance improvements

---

**Built with ❤️ using Django and PostgreSQL**
