@echo off
REM Start DayFlow HRMS server

echo ================================
echo Starting DayFlow HRMS Server
echo ================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start Django development server
python manage.py runserver

pause
