@echo off
echo ========================================
echo DayFlow HRMS - Setup Script
echo ========================================
echo.

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/5] Creating upload directories...
if not exist "app\static\uploads\profiles" mkdir app\static\uploads\profiles

echo [5/5] Setup complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo 1. Create MySQL database: dayflow_hrms
echo 2. Update database credentials in config.py
echo 3. Run: python init_db.py (to initialize database)
echo 4. Run: python run.py (to start the application)
echo.
echo Default Login:
echo   Admin - admin@dayflow.com / admin123
echo   Employee - alice@dayflow.com / employee123
echo ========================================
pause
