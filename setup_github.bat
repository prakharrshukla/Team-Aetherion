@echo off
echo.
echo =====================================================
echo    TEAM-AETHERION - UOWD AEROSPACE MACHINE VISION
echo              GITHUB REPOSITORY SETUP
echo =====================================================
echo.

echo Initializing Git repository...
git init
if errorlevel 1 (
    echo ERROR: Git initialization failed. Make sure Git is installed.
    pause
    exit /b 1
)

echo.
echo Adding all files to Git...
git add .
if errorlevel 1 (
    echo ERROR: Failed to add files to Git.
    pause
    exit /b 1
)

echo.
echo Creating initial commit...
git commit -m "Initial release of Team-Aetherion UOWD Aerospace Machine Vision System"
if errorlevel 1 (
    echo ERROR: Failed to create commit.
    pause
    exit /b 1
)

echo.
echo =====================================================
echo    GIT REPOSITORY SUCCESSFULLY INITIALIZED!
echo =====================================================
echo.
echo Your local repository is ready!
echo.
echo NEXT STEPS:
echo 1. Create a new repository on GitHub
echo 2. Copy the repository URL
echo 3. Run: git remote add origin [YOUR_GITHUB_URL]
echo 4. Run: git push -u origin main
echo.
echo OR use the GitHub Desktop app to publish this repository.
echo.
pause
