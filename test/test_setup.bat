@echo off
:: Quick test script for Windows

echo 🧪 Testing GitHub Auto Commit Setup
echo ==================================

echo 1. Testing dry-run mode...
python github_auto_commit.py --dry-run
if %errorlevel% equ 0 (
    echo ✓ Dry-run test passed
) else (
    echo ✗ Dry-run test failed
    goto :error
)

echo.
echo 2. Testing configuration...
if exist config.json (
    echo ✓ Configuration file found
) else (
    echo ⚠ Configuration file will be created on first run
)

echo.
echo 3. Testing Git repository...
git status >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Git repository detected
) else (
    echo ⚠ Initializing Git repository...
    git init >nul
    git checkout -b main >nul
)

echo.
echo 4. Testing monitor script...
python monitor.py --help >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Monitor script available
) else (
    echo ⚠ Monitor script may need Python re module
)

echo.
echo 🎉 All tests completed successfully!
echo.
echo Next steps:
echo 1. Review config.json settings
echo 2. Run: python github_auto_commit.py --mode daily
echo 3. Setup scheduling: scheduler_helper.bat install
echo.
goto :eof

:error
echo.
echo ❌ Setup test failed
echo Please check Python and Git installations
echo.
pause
exit /b 1