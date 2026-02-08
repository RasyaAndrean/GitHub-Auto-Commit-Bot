@echo off
:: Scheduling helper script for Windows

set SCRIPT_DIR=%~dp0
set SCRIPT_PATH=%SCRIPT_DIR%github_auto_commit.py
set CONFIG_PATH=%SCRIPT_DIR%config.json

goto %1

:install
echo Installing Task Scheduler job...
call :create_batch_file
call :setup_task_scheduler
goto :eof

:remove
echo Removing Task Scheduler job...
schtasks /delete /tn "GitHubAutoCommit" /f >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Task Scheduler job removed
) else (
    echo ⚠ No task found or failed to remove
)
del "%SCRIPT_DIR%run_auto_commit.bat" >nul 2>&1
goto :eof

:status
echo Current Task Scheduler jobs:
echo ============================
schtasks /query /tn "GitHubAutoCommit" >nul 2>&1
if %errorlevel% equ 0 (
    schtasks /query /tn "GitHubAutoCommit" /fo LIST
) else (
    echo No GitHub auto commit task found
)
goto :eof

:list
echo Scheduled GitHub Auto Commit Tasks:
echo ===================================
schtasks /query /tn "GitHubAutoCommit" >nul 2>&1
if %errorlevel% equ 0 (
    schtasks /query /tn "GitHubAutoCommit" /fo TABLE
) else (
    echo No scheduled tasks found
)
goto :eof

:run
shift
echo Running GitHub Auto Commit script...
python "%SCRIPT_PATH%" %*
goto :eof

:test
echo Running in dry-run mode...
python "%SCRIPT_PATH%" --dry-run
goto :eof

:help
echo GitHub Auto Commit Scheduler Helper
echo ==================================
echo Usage: scheduler_helper.bat [command]
echo.
echo Commands:
echo   install     - Install/update Task Scheduler job
echo   remove      - Remove Task Scheduler job
echo   status      - Show current task status
echo   list        - List all scheduled tasks
echo   run         - Run script manually
echo   test        - Run in dry-run mode
echo   help        - Show this help
echo.
echo Examples:
echo   scheduler_helper.bat install
echo   scheduler_helper.bat run --mode backfill --days 30
goto :eof

:create_batch_file
echo Creating batch file for Task Scheduler...
echo @echo off > "%SCRIPT_DIR%run_auto_commit.bat"
echo cd /d "%SCRIPT_DIR%" >> "%SCRIPT_DIR%run_auto_commit.bat"
echo python github_auto_commit.py --mode daily --config config.json >> "%SCRIPT_DIR%run_auto_commit.bat"
echo exit /b %%ERRORLEVEL%% >> "%SCRIPT_DIR%run_auto_commit.bat"
goto :eof

:setup_task_scheduler
:: Generate random time (between 7 AM and 10 PM)
set /a HOUR=%RANDOM%%%15+7
set /a MINUTE=%RANDOM%%%60

:: Format time as HH:MM
if %MINUTE% lss 10 (
    set TIME_STR=%HOUR%:0%MINUTE%
) else (
    set TIME_STR=%HOUR%:%MINUTE%
)

:: Create scheduled task
schtasks /create /tn "GitHubAutoCommit" /tr "\"%SCRIPT_DIR%run_auto_commit.bat\"" /sc daily /st %TIME_STR% /f >nul 2>&1

if %errorlevel% equ 0 (
    echo ✓ Task Scheduler job installed for %TIME_STR% daily
    echo Log file: %SCRIPT_DIR%auto_commit.log
) else (
    echo ✗ Failed to create scheduled task
    echo You can try running as administrator
)
goto :eof

:: Default to help if no valid command
if "%1"=="" goto help
echo Unknown command: %1
echo Use 'help' for available commands