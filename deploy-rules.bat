@echo off
echo ========================================
echo Deploying Firebase Security Rules
echo ========================================
echo.
echo This will deploy your security rules to Firebase.
echo.

echo Deploying Firestore rules...
call firebase deploy --only firestore:rules
if %errorlevel% neq 0 (
    echo [ERROR] Failed to deploy Firestore rules
    pause
    exit /b 1
)
echo [OK] Firestore rules deployed!
echo.

echo Deploying Storage rules...
call firebase deploy --only storage
if %errorlevel% neq 0 (
    echo [ERROR] Failed to deploy Storage rules
    pause
    exit /b 1
)
echo [OK] Storage rules deployed!
echo.

echo ========================================
echo [SUCCESS] All rules deployed!
echo ========================================
echo.
echo Your Firebase security is now configured.
echo.
echo Next step:
echo Double-click start.bat to launch your app!
echo.
pause
