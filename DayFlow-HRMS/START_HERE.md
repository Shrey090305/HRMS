# 🚀 START HERE - DayFlow HRMS

## Welcome to DayFlow HRMS!

This is your complete Human Resource Management System. Follow these simple steps to get started.

---

## 📋 Prerequisites Check

Before starting, make sure you have:
- [ ] Python 3.8+ installed
- [ ] MySQL 5.7+ installed
- [ ] MySQL root password ready

---

## 🎯 Quick Start (3 Steps)

### Step 1: Setup Database (2 minutes)

Open MySQL and run:
```sql
CREATE DATABASE dayflow_hrms;
```

Then update `config.py` line 7:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:YOUR_PASSWORD@localhost/dayflow_hrms'
```
Replace `YOUR_PASSWORD` with your MySQL password.

---

### Step 2: Install & Initialize (2 minutes)

**Option A - Automated (Windows):**
```bash
# Double-click setup.bat
```

**Option B - Manual:**
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database with sample data
python init_db.py
```

---

### Step 3: Run Application (1 minute)

```bash
# Make sure virtual environment is activated
python run.py
```

Open browser: **http://localhost:5000**

---

## 🔐 Login & Explore

### Try Admin Features
```
Email: admin@dayflow.com
Password: admin123
```

**What to do:**
1. View dashboard statistics
2. Go to "Employees" → See all staff
3. Go to "Leave Requests" → Approve/reject
4. Check "Reports" → View charts

---

### Try Employee Features
```
Email: alice@dayflow.com
Password: employee123
```

**What to do:**
1. Click "Check In" button
2. Go to "Leave" → Apply for leave
3. View your payroll
4. Update your profile

---

## 📚 Documentation Guide

| File | Purpose | When to Read |
|------|---------|--------------|
| **QUICKSTART.md** | 5-minute tutorial | First time setup |
| **README.md** | Complete guide | For full documentation |
| **PROJECT_SUMMARY.md** | Feature overview | To understand what's included |

---

## ✅ Verify Installation

Run verification script:
```bash
python verify_setup.py
```

This checks if all files are in place.

---

## 🎯 Your First Actions

### 1️⃣ Test Employee Workflow
- Login as alice@dayflow.com
- Check in for attendance
- Apply for 3-day leave
- View payroll details

### 2️⃣ Test Admin Workflow
- Login as admin@dayflow.com
- View the leave request from Alice
- Approve it with a comment
- Check reports → Attendance chart

### 3️⃣ Add Your Own Employee
- As admin, go to Employees
- Click "Add Employee"
- Fill details and save
- Try logging in with new credentials

---

## 🔧 Troubleshooting

### "Can't connect to database"
→ Check if MySQL is running  
→ Verify credentials in config.py  
→ Ensure database exists

### "ModuleNotFoundError"
→ Run: `pip install -r requirements.txt`  
→ Make sure virtual environment is activated

### "Port 5000 already in use"
→ Edit run.py, change port to 5001  
→ Or stop the process using port 5000

### "Template not found"
→ Make sure you're in project root directory  
→ Run: `python verify_setup.py`

---

## 💡 Tips for Success

1. **Start with sample data** - The init_db.py creates 5 employees with records
2. **Use Chrome/Firefox** - For best experience
3. **Test both roles** - Use incognito mode for testing admin + employee together
4. **Check console** - Press F12 in browser to see any JavaScript errors
5. **Read code comments** - All files have helpful comments

---

## 🎓 Learning Path

**Day 1:** Setup + Basic Navigation
- Install and run
- Login as both roles
- Explore dashboards

**Day 2:** Core Features
- Attendance check-in/out
- Leave application and approval
- Profile updates

**Day 3:** Admin Tasks
- Add employees
- Manage payroll
- View reports

**Day 4:** Advanced
- Customize CSS
- Add new features
- Deploy to production

---

## 📊 What's Included

✅ **Complete Application**
- 13 Python files
- 25 HTML templates
- Custom CSS & JavaScript
- Sample data script

✅ **All Features Working**
- Authentication
- Dashboards (Admin & Employee)
- Attendance Management
- Leave Management
- Payroll Management
- Reports with Charts

✅ **Documentation**
- README (complete guide)
- QUICKSTART (5-min tutorial)
- PROJECT_SUMMARY (overview)
- Code comments

✅ **Tools**
- setup.bat (Windows automation)
- verify_setup.py (check installation)
- create_dirs.py (create folders)

---

## 🎨 Customization Ideas

Want to make it yours?

**Easy:**
- Change colors in `app/static/css/style.css`
- Update company name in templates
- Add your logo

**Medium:**
- Add new leave types
- Create department-wise reports
- Add email notifications

**Advanced:**
- Integrate with payroll API
- Add biometric attendance
- Create mobile app

---

## 🆘 Need Help?

1. **Check verify_setup.py output** - Shows what's missing
2. **Read error messages** - They usually tell you what's wrong
3. **Check browser console** - For JavaScript errors (F12)
4. **Review README.md** - Has detailed troubleshooting
5. **Test with sample data** - Before adding your own

---

## 🎉 You're Ready!

Everything is set up and ready to use. The application includes:

- 5 sample employees with attendance records
- 3 leave requests in different states
- Payroll records for last 3 months
- Working charts and reports

**Start with:**
```bash
python run.py
```

Then open: **http://localhost:5000**

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Install dependencies | `pip install -r requirements.txt` |
| Check setup | `python verify_setup.py` |
| Initialize database | `python init_db.py` |
| Run application | `python run.py` |
| Create directories | `python create_dirs.py` |

---

**Good luck with your HRMS! 🚀**

*Built with Flask, MySQL, Bootstrap, and ❤️*
