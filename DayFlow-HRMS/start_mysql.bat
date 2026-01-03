@echo off
echo Starting MySQL Service...
net start MySQL57
if %errorlevel% == 0 (
    echo MySQL started successfully!
) else (
    echo Failed to start MySQL. Please run this script as Administrator.
    echo Right-click start_mysql.bat and select "Run as administrator"
)
pause
