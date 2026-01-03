@echo off
REM Setup script for DayFlow HRMS on Windows

echo ================================
echo DayFlow HRMS Setup Script
echo ================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from https://www.python.org
    pause
    exit /b 1
)

echo [1/7] Python found!
echo.

REM Create virtual environment
echo [2/7] Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)
echo.

REM Activate virtual environment and install dependencies
echo [3/7] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo.

REM Check PostgreSQL connection
echo [4/7] Checking PostgreSQL...
echo Please ensure PostgreSQL is running and you have created the database.
echo Run this in PostgreSQL:
echo    CREATE DATABASE dayflow_hrms;
echo.
pause

REM Run migrations
echo [5/7] Running database migrations...
python manage.py makemigrations
python manage.py migrate
echo.

REM Create superuser
echo [6/7] Creating superuser account...
echo Please enter admin credentials:
python manage.py createsuperuser
echo.

REM Collect static files
echo [7/7] Collecting static files...
python manage.py collectstatic --noinput
echo.

echo ================================
echo Setup completed successfully!
echo ================================
echo.
echo To start the server, run:
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Then open your browser to: http://localhost:8000
echo.
pause
