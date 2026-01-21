@echo off
echo ========================================
echo Firebase Initialization
echo ========================================
echo.
echo IMPORTANT: Make sure you completed the Firebase Console setup!
echo (If not, open FIREBASE_CONSOLE_SETUP.md and follow the steps)
echo.
echo This script will:
echo 1. Log you into Firebase (opens browser)
echo 2. Connect this project to your Firebase project
echo 3. Set up Firestore and Storage locally
echo.
pause

echo.
echo Step 1: Logging into Firebase...
echo A browser window will open. Please log in with your Google account.
echo.
call firebase login
if %errorlevel% neq 0 (
    echo [ERROR] Firebase login failed
    pause
    exit /b 1
)

echo.
echo [OK] Logged in successfully!
echo.

echo Step 2: Linking to your Firebase project...
echo.
echo When prompted, select "Use an existing project"
echo Then select: lifelogger-e6ecd
echo.
pause
call firebase use --add
if %errorlevel% neq 0 (
    echo [ERROR] Failed to link project
    pause
    exit /b 1
)

echo.
echo [OK] Project linked!
echo.

echo Step 3: Initializing Firestore...
echo When prompted:
echo - Use an existing project
echo - Firestore rules file: Press Enter (use default: firestore.rules)
echo - Firestore indexes file: Press Enter (use default: firestore.indexes.json)
echo - Do NOT overwrite existing files
echo.
pause
call firebase init firestore
if %errorlevel% neq 0 (
    echo [ERROR] Firestore initialization failed
    pause
    exit /b 1
)

echo.
echo [OK] Firestore initialized!
echo.

echo Step 4: Initializing Storage...
echo When prompted:
echo - Storage rules file: Press Enter (use default: storage.rules)
echo - Do NOT overwrite existing file
echo.
pause
call firebase init storage
if %errorlevel% neq 0 (
    echo [ERROR] Storage initialization failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo [SUCCESS] Firebase initialized!
echo ========================================
echo.
echo Next step:
echo Double-click deploy-rules.bat to deploy your security rules
echo.
pause
