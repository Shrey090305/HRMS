# DayFlow HRMS - Human Resource Management System

A complete, production-ready Human Resource Management System built with Flask, MySQL, HTML, CSS, JavaScript, and Bootstrap.

## 🚀 Features

### Authentication & Authorization
- **Sign Up & Sign In** with email and password
- **Password Hashing** using bcrypt for security
- **Session-based Authentication** with Flask-Login
- **Role-based Access Control** (Admin & Employee)
- Automatic redirection based on user role

### Employee Dashboard
- Personal profile card with profile picture
- Today's attendance status
- Leave request summary
- Latest payroll information
- Recent attendance history (last 7 days)

### Admin Dashboard
- Organization overview statistics
- Total employees count
- Today's attendance summary
- Pending leave requests
- Recent employees list
- Recent leave requests

### Employee Profile Management
- View personal, job, and contact information
- Edit limited fields (employees can update phone, address, profile picture)
- Admin can edit all employee fields
- Profile picture upload support (max 5MB)

### Attendance Management
- **Employee Features:**
  - Daily check-in/check-out with timestamps
  - View attendance history (last 7 days)
  - Real-time status updates
  
- **Admin Features:**
  - View all employee attendance
  - Filter by date
  - Mark attendance manually
  - Daily attendance statistics (Present, Absent, Half-day, Leave)

### Leave Management
- **Employee Features:**
  - Apply for leave with type, date range, and reason
  - Leave types: Sick, Casual, Annual, Emergency
  - View all leave requests and their status
  - Track approval/rejection with admin comments
  
- **Admin Features:**
  - View all leave requests with filtering
  - Approve/Reject leave requests
  - Add comments to leave decisions
  - Leave statistics dashboard

### Payroll Management
- **Employee Features:**
  - View salary details (read-only)
  - Basic salary, allowances, deductions breakdown
  - Net salary calculation
  - Payment status tracking
  
- **Admin Features:**
  - Add new payroll records
  - Edit existing payroll
  - Manage payment status
  - Record payment dates
  - Search payroll by employee

### Reports & Analytics
- **Attendance Reports:**
  - Date range filtering
  - Employee-wise attendance summary
  - Attendance percentage calculation
  - Present/Absent/Half-day/Leave breakdown
  
- **Leave Reports:**
  - Year-wise filtering
  - Employee-wise leave summary
  - Approved days tracking
  - Pending and rejected requests count
  
- **Interactive Charts:**
  - Attendance trend (last 7 days) - Line chart
  - Leave types distribution - Doughnut chart
  - Real-time data using Chart.js

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0** - Web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **Flask-Login** - User session management
- **Flask-Bcrypt** - Password hashing
- **PyMySQL** - MySQL database connector

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling with custom design
- **JavaScript (ES6)** - Client-side functionality
- **Bootstrap 5.3** - Responsive UI framework
- **Font Awesome 6.4** - Icons
- **Chart.js 4.4** - Interactive charts

### Database
- **MySQL** - Relational database
- Properly normalized schema with foreign keys
- Cascade delete for referential integrity

## 📁 Project Structure

```
DayFlow-HRMS/
│
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── models.py                # Database models
│   │
│   ├── routes/
│   │   ├── auth.py             # Authentication routes
│   │   ├── admin.py            # Admin routes
│   │   ├── employee.py         # Employee routes
│   │   ├── attendance.py       # Attendance management
│   │   ├── leave.py            # Leave management
│   │   ├── payroll.py          # Payroll management
│   │   └── reports.py          # Reports and analytics
│   │
│   ├── templates/
│   │   ├── base.html           # Base template
│   │   ├── auth/               # Authentication pages
│   │   ├── employee/           # Employee pages
│   │   ├── admin/              # Admin pages
│   │   ├── attendance/         # Attendance pages
│   │   ├── leave/              # Leave pages
│   │   ├── payroll/            # Payroll pages
│   │   └── reports/            # Reports pages
│   │
│   └── static/
│       ├── css/
│       │   └── style.css       # Custom CSS
│       ├── js/
│       │   └── script.js       # Custom JavaScript
│       └── uploads/            # User uploads (profile pictures)
│           └── profiles/
│
├── config.py                   # Configuration settings
├── run.py                      # Application entry point
├── init_db.py                  # Database initialization script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)

### Step 1: Clone or Extract the Project
```bash
cd DayFlow-HRMS
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure MySQL Database

1. **Create MySQL Database:**
```sql
CREATE DATABASE dayflow_hrms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. **Update Database Configuration:**

Edit `config.py` and update the database URI:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/dayflow_hrms'
```

Replace `username` and `password` with your MySQL credentials.

**Example:**
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mypassword@localhost/dayflow_hrms'
```

### Step 5: Initialize Database with Sample Data
```bash
python init_db.py
```

This will:
- Create all database tables
- Insert sample data (1 admin, 5 employees)
- Create sample attendance records
- Create sample leave requests
- Create sample payroll records

### Step 6: Run the Application
```bash
python run.py
```

The application will start on `http://localhost:5000`

## 🔐 Default Login Credentials

### Admin Account
- **Email:** admin@dayflow.com
- **Password:** admin123

### Employee Accounts
- **Email:** alice@dayflow.com (or bob@dayflow.com, carol@dayflow.com, david@dayflow.com, emma@dayflow.com)
- **Password:** employee123

## 📖 Usage Guide

### For Employees

1. **Login:** Use your email and password to sign in
2. **Dashboard:** View your profile, attendance, leave status, and payroll
3. **Attendance:**
   - Click "Check In" button to mark your arrival
   - Click "Check Out" button when leaving
   - View your attendance history
4. **Leave:**
   - Click "Apply for Leave" to submit a new request
   - Select leave type, dates, and provide reason
   - Track status of your requests
5. **Profile:**
   - View your complete profile
   - Edit phone number, address, and profile picture
6. **Payroll:**
   - View your salary details
   - Check payment status

### For Admins

1. **Login:** Use admin credentials
2. **Dashboard:** Overview of organization metrics
3. **Employee Management:**
   - View all employees
   - Add new employees
   - Edit employee details
   - Deactivate employees
4. **Attendance Management:**
   - View attendance for any date
   - See daily statistics
   - Mark attendance manually if needed
5. **Leave Management:**
   - View all leave requests
   - Filter by status (Pending/Approved/Rejected)
   - Approve or reject requests with comments
6. **Payroll Management:**
   - Add payroll for employees
   - Edit salary components
   - Update payment status
   - Record payment dates
7. **Reports:**
   - Generate attendance reports
   - View leave reports
   - Analyze trends with charts

## 🔒 Security Features

- **Password Hashing:** All passwords are hashed using bcrypt
- **Session Management:** Secure session-based authentication
- **Role-based Access:** Strict separation between admin and employee access
- **SQL Injection Prevention:** Using SQLAlchemy ORM
- **CSRF Protection:** Built into Flask forms
- **File Upload Validation:** Size and type restrictions for profile pictures

## 🎨 Design Features

- **Responsive Design:** Works on desktop, tablet, and mobile
- **Clean UI:** Modern, professional interface
- **Intuitive Navigation:** Easy-to-use menu system
- **Visual Feedback:** Alerts, badges, and color-coded status
- **Interactive Charts:** Real-time data visualization
- **Card-based Layout:** Organized information display

## 🚀 Advanced Features

- **Pagination:** For large datasets in tables
- **Search Functionality:** Quick employee and payroll search
- **Date Filtering:** For reports and attendance
- **Auto-calculation:** Net salary calculation in payroll
- **Real-time Updates:** AJAX for check-in/check-out
- **Form Validation:** Client and server-side validation

## 🛠️ Customization

### Change Secret Key
Edit `config.py`:
```python
SECRET_KEY = 'your-unique-secret-key-here'
```

### Change Upload Settings
Edit `config.py`:
```python
UPLOAD_FOLDER = 'your/upload/path'
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
```

### Modify Database Settings
Edit `config.py` to change database connection parameters.

### Customize Styles
Edit `app/static/css/style.css` to modify colors, fonts, and layouts.

## 📊 Database Schema

### Users Table
- id, employee_id, email, password, role
- first_name, last_name, phone, address
- date_of_birth, gender, profile_picture
- department, designation, joining_date, employment_type
- is_active, created_at, updated_at

### Attendance Table
- id, user_id (FK), date
- check_in, check_out, status, remarks
- created_at, updated_at

### Leaves Table
- id, user_id (FK), leave_type
- start_date, end_date, days, reason
- status, admin_comments
- applied_at, reviewed_at

### Payroll Table
- id, user_id (FK), month, year
- basic_salary, allowances, deductions, net_salary
- payment_date, payment_status
- created_at, updated_at

## 🐛 Troubleshooting

### Database Connection Error
- Verify MySQL is running
- Check database credentials in `config.py`
- Ensure database exists

### Import Errors
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

### Template Not Found
- Ensure you're in the project root directory
- Check file paths in route handlers

### Port Already in Use
- Change port in `run.py`: `app.run(port=5001)`
- Or stop the process using port 5000

## 📝 API Endpoints

### Authentication
- `GET/POST /signup` - User registration
- `GET/POST /signin` - User login
- `GET /logout` - User logout

### Employee
- `GET /employee/dashboard` - Employee dashboard
- `GET /employee/profile` - View profile
- `GET/POST /employee/profile/edit` - Edit profile

### Admin
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/employees` - List employees
- `GET /admin/employee/<id>` - Employee details
- `GET/POST /admin/employee/<id>/edit` - Edit employee
- `GET/POST /admin/employee/add` - Add employee

### Attendance
- `GET /attendance/` - View attendance
- `POST /attendance/checkin` - Check in
- `POST /attendance/checkout` - Check out

### Leave
- `GET /leave/` - List leaves
- `GET/POST /leave/apply` - Apply for leave
- `GET /leave/<id>/detail` - Leave details
- `POST /leave/<id>/review` - Review leave (admin)

### Payroll
- `GET /payroll/` - List payroll
- `GET/POST /payroll/add` - Add payroll (admin)
- `GET/POST /payroll/<id>/edit` - Edit payroll (admin)
- `GET /payroll/<id>/detail` - Payroll details

### Reports
- `GET /reports/` - Reports dashboard
- `GET /reports/attendance` - Attendance report
- `GET /reports/leave` - Leave report
- `GET /reports/api/attendance-chart` - Chart data
- `GET /reports/api/leave-chart` - Chart data

## 🤝 Contributing

This is a complete production-ready application. Feel free to:
- Add new features
- Improve existing functionality
- Fix bugs
- Enhance UI/UX
- Add more reports

## 📄 License

This project is created for educational and commercial purposes.

## 👨‍💻 Author

Built with ❤️ as a complete HRMS solution

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review the code comments
- Test with the provided sample data

---

**Version:** 1.0.0  
**Last Updated:** January 2026  
**Status:** Production Ready ✅
