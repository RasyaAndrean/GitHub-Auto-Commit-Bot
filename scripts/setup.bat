@echo off
:: Setup script for GitHub Auto Commit (Windows)
setlocal enabledelayedexpansion

echo 🚀 Setting up GitHub Auto Commit Script...
echo ==========================================

:: Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Python 3 is not installed or not in PATH
    echo Please install Python 3 from https://www.python.org/
    pause
    exit /b 1
)
echo ✓ Found Python

:: Check Git installation
echo Checking Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)
echo ✓ Found Git

:: Create initial files
echo Creating initial tracking files...
echo # Activity Log > activity_log.txt
echo This file tracks automated activities. >> activity_log.txt
echo. >> activity_log.txt

echo # Progress Tracker > progress_tracker.md
echo. >> progress_tracker.md
echo ## Today's Progress >> progress_tracker.md
echo. >> progress_tracker.md

echo # Development Notes > development_notes.txt
echo Automated development tracking file. >> development_notes.txt
echo. >> development_notes.txt

echo # Changelog > changelog.md
echo. >> changelog.md
echo All changes are tracked automatically. >> changelog.md
echo. >> changelog.md

echo ✓ Initial files created

:: Setup Task Scheduler
echo.
echo Setting up scheduled execution...
choice /C YN /M "Would you like to setup automatic daily execution"
if errorlevel 2 (
    echo Skipping Task Scheduler setup.
    goto test_setup
)

:: Create batch file for task scheduler
echo @echo off > run_auto_commit.bat
echo cd /d "%~dp0" >> run_auto_commit.bat
echo python github_auto_commit.py --mode daily >> run_auto_commit.bat
echo exit /b %%ERRORLEVEL%% >> run_auto_commit.bat

:: Setup Task Scheduler using PowerShell
powershell -Command ^
"$action = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument '/c \"%~dp0run_auto_commit.bat\"'; ^
$trigger = New-ScheduledTaskTrigger -Daily -At \"9:00AM\"; ^
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries; ^
Register-ScheduledTask -TaskName 'GitHubAutoCommit' -Action $action -Trigger $trigger -Settings $settings -Description 'Automatic GitHub commits'"

if %errorlevel% equ 0 (
    echo ✓ Task Scheduler job created (runs daily at 9:00 AM)
    echo You can modify the schedule through Task Scheduler GUI
) else (
    echo ⚠ Failed to create scheduled task. You can run manually.
)

:test_setup
echo.
echo Testing the setup...
python github_auto_commit.py --mode daily --dry-run
if %errorlevel% equ 0 (
    echo ✓ Setup test completed successfully!
) else (
    echo ✗ Setup test failed
    pause
    exit /b 1
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo Next steps:
echo   1. Review config.json to customize settings
echo   2. Run manually: python github_auto_commit.py --mode daily
echo   3. For backfill: python github_auto_commit.py --mode backfill --days 30
echo   4. Check auto_commit.log for activity logs
echo.
echo Remember to push to your GitHub repository:
echo   git remote add origin https://github.com/username/repository.git
echo   git push -u origin main
echo.
pause