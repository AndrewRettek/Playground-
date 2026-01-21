@echo off
echo ========================================
echo Life Logger - Setup Script
echo ========================================
echo.

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed!
    echo.
    echo Please install Node.js first:
    echo 1. Open INSTALL_NODEJS.md for instructions
    echo 2. Or go to: https://nodejs.org/
    echo 3. Download the LTS version and run the installer
    echo 4. Then run this script again
    echo.
    pause
    exit /b 1
)

echo [OK] Node.js is installed
node --version
echo.

echo Installing Firebase CLI globally...
echo This may take a few minutes...
call npm install -g firebase-tools
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Firebase CLI
    pause
    exit /b 1
)
echo.

echo [OK] Firebase CLI installed
echo.

echo Installing project dependencies...
echo This will take a few minutes...
call npm run install:all
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo ========================================
echo [SUCCESS] Setup complete!
echo ========================================
echo.
echo Next steps:
echo 1. Open FIREBASE_CONSOLE_SETUP.md in your browser or text editor
echo 2. Follow the steps to enable Firebase services (takes 5 minutes)
echo 3. Then double-click firebase-init.bat
echo.
pause
