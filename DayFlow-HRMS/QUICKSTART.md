# DayFlow HRMS - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install MySQL
If you don't have MySQL installed:
- Download from: https://dev.mysql.com/downloads/installer/
- Install and remember your root password

### Step 2: Create Database
Open MySQL Command Line or MySQL Workbench and run:
```sql
CREATE DATABASE dayflow_hrms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Step 3: Configure Database Connection
Open `config.py` and update line 7:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:YOUR_PASSWORD@localhost/dayflow_hrms'
```
Replace `YOUR_PASSWORD` with your MySQL root password.

### Step 4: Run Setup (Windows)
Double-click `setup.bat` or run in terminal:
```bash
setup.bat
```

This will:
- Create virtual environment
- Install all dependencies
- Create necessary directories

### Step 5: Initialize Database
Open terminal in project folder and run:
```bash
# Activate virtual environment first
venv\Scripts\activate

# Initialize database with sample data
python init_db.py
```

### Step 6: Start Application
```bash
python run.py
```

### Step 7: Access Application
Open your browser and go to:
```
http://localhost:5000
```

## 🔐 Login Credentials

### Admin Access
```
Email: admin@dayflow.com
Password: admin123
```

### Employee Access
```
Email: alice@dayflow.com
Password: employee123
```

(Also available: bob@dayflow.com, carol@dayflow.com, david@dayflow.com, emma@dayflow.com)

## ✅ What You Can Do

### As Employee:
1. ✓ Check in/out for attendance
2. ✓ Apply for leave
3. ✓ View payroll
4. ✓ Update profile
5. ✓ View attendance history

### As Admin:
1. ✓ Manage all employees
2. ✓ View/approve leave requests
3. ✓ Manage attendance
4. ✓ Handle payroll
5. ✓ Generate reports
6. ✓ View analytics

## 🎯 First Actions to Try

### Employee Dashboard
1. Login as employee (alice@dayflow.com)
2. Click "Check In" button
3. Go to Leave → Apply for Leave
4. Fill the form and submit
5. View your payroll records

### Admin Dashboard
1. Login as admin
2. Go to Leave Requests → View pending requests
3. Approve/Reject a leave
4. Go to Employees → Add new employee
5. View Reports → Check attendance chart

## 📱 Features Overview

| Module | Employee | Admin |
|--------|----------|-------|
| Dashboard | ✓ | ✓ |
| Profile | View + Edit Limited | View + Edit All |
| Attendance | Check-in/out + View Own | View All + Mark |
| Leave | Apply + View Own | View All + Approve/Reject |
| Payroll | View Only | Add + Edit + View All |
| Reports | ✗ | Generate All Reports |

## 🔧 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Access denied for user"
- Check MySQL username and password in `config.py`
- Ensure MySQL service is running

### "Can't connect to MySQL server"
- Start MySQL service
- Check if MySQL is running on port 3306

### Port 5000 already in use
Edit `run.py` line 10:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📚 Learn More

See `README.md` for:
- Complete feature list
- Detailed installation guide
- API documentation
- Database schema
- Customization options

## 🎓 Tutorial: Complete Workflow

### Scenario: New Employee Leave Request

1. **Admin adds employee:**
   - Login as admin
   - Employees → Add Employee
   - Fill details and save

2. **Employee logs in:**
   - Use credentials from admin
   - View dashboard

3. **Employee applies for leave:**
   - Leave → Apply for Leave
   - Select dates and type
   - Submit request

4. **Admin reviews leave:**
   - See notification on dashboard
   - Go to Leave Requests
   - View details
   - Approve/Reject with comments

5. **Employee checks status:**
   - Go to Leave section
   - See approved/rejected status

## 💡 Tips

- **Sample Data:** The init_db.py creates 5 sample employees with attendance and payroll data
- **Testing:** Use different browsers or incognito mode to test both admin and employee roles
- **Backup:** Regularly backup your MySQL database
- **Production:** Change SECRET_KEY in config.py before deploying

## 🎨 Customize

### Change Theme Colors
Edit `app/static/css/style.css` - lines 2-7

### Modify Dashboard
Edit templates in `app/templates/employee/` or `app/templates/admin/`

### Add Features
- Create new routes in `app/routes/`
- Add templates in `app/templates/`
- Update models in `app/models.py`

## 📞 Need Help?

1. Check README.md for detailed documentation
2. Review code comments in Python files
3. Test with sample data first
4. Check browser console for JavaScript errors

---

**Ready to go!** 🚀

Start with the employee dashboard to see the user experience, then explore admin features.
