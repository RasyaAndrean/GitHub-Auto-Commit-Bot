@echo off
:: GitHub Auto Commit Launcher for Windows

echo 🚀 GitHub Auto Commit Bot Launcher
echo ====================================

:menu
echo.
echo Select an option:
echo 1. Quick Setup
echo 2. Test Installation
echo 3. Run Daily Commits
echo 4. Backfill History
echo 5. Monitor Activity
echo 6. Manage Scheduling
echo 7. GitHub Auto Bot (NEW) - Interactive Menu
echo 8. View Documentation
echo 9. Exit
echo.

set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto test
if "%choice%"=="3" goto daily
if "%choice%"=="4" goto backfill
if "%choice%"=="5" goto monitor
if "%choice%"=="6" goto schedule
if "%choice%"=="7" goto github_bot
if "%choice%"=="8" goto docs
if "%choice%"=="9" goto exit

echo Invalid choice. Please try again.
goto menu

:setup
echo.
echo 🔧 Running Setup...
cd scripts
call setup.bat
cd ..
goto menu

:test
echo.
echo 🧪 Testing Installation...
cd scripts
python github_auto_commit.py --dry-run
cd ..
pause
goto menu

:daily
echo.
echo 📅 Running Daily Commits...
cd scripts
python github_auto_commit.py --mode daily
cd ..
pause
goto menu

:backfill
set /p days="Enter number of days to backfill: "
echo.
echo ⏪ Backfilling %days% days...
cd scripts
python github_auto_commit.py --mode backfill --days %days%
cd ..
pause
goto menu

:monitor
echo.
echo 📊 Monitoring Activity...
cd scripts
python monitor.py
cd ..
pause
goto menu

:schedule
echo.
echo ⏰ Schedule Management
echo 1. Install scheduled task
echo 2. Remove scheduled task
echo 3. Check task status
echo 4. Back to main menu
set /p sched_choice="Enter choice (1-4): "

if "%sched_choice%"=="1" (
    cd scripts
    scheduler_helper.bat install
    cd ..
) else if "%sched_choice%"=="2" (
    cd scripts
    scheduler_helper.bat remove
    cd ..
) else if "%sched_choice%"=="3" (
    cd scripts
    scheduler_helper.bat status
    cd ..
) else if "%sched_choice%"=="4" (
    goto menu
) else (
    echo Invalid choice.
)
pause
goto schedule

:github_bot
echo.
echo 🤖 Starting GitHub Auto Bot...
echo This will open an interactive menu for GitHub automation
echo.
python main.py
pause
goto menu

:docs
echo.
echo 📖 Opening Documentation...
echo Check the docs/ folder for detailed documentation
echo Quick Start Guide: docs/QUICK_START.md
echo Full Documentation: docs/README.md
echo.
pause
goto menu

:exit
echo.
echo 👋 Goodbye!
exit /b 0