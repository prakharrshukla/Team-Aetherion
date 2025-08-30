@echo off
title Team-Aetherion - UOWD Aerospace Machine Vision System

:menu
cls
echo ============================================================
echo  TEAM-AETHERION - UOWD AEROSPACE MACHINE VISION LAUNCHER
echo ============================================================
echo.
echo Select an option:
echo.
echo 1. Run System Test
echo 2. Run Demo (Sample Objects)
echo 3. Start Basic Machine Vision
echo 4. Start Advanced Machine Vision
echo 5. View README Documentation
echo 6. Exit
echo.
echo ============================================================

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto test
if "%choice%"=="2" goto demo  
if "%choice%"=="3" goto basic
if "%choice%"=="4" goto advanced
if "%choice%"=="5" goto readme
if "%choice%"=="6" goto exit

echo Invalid choice. Please try again.
pause
goto menu

:test
cls
echo Running System Test...
echo.
python test_system.py
echo.
pause
goto menu

:demo
cls
echo Running Demo...
echo.
python demo.py
echo.
pause
goto menu

:basic
cls
echo Starting Basic Machine Vision System...
echo Press 'q' in the camera window to quit
echo Press 's' to save screenshots
echo.
python machine_vision.py
echo.
pause
goto menu

:advanced
cls
echo Starting Advanced Machine Vision System...
echo Press 'q' to quit, 's' to save, 'd' to export data
echo Press 1-4 to show different edge detection methods
echo.
python advanced_machine_vision.py
echo.
pause
goto menu

:readme
cls
echo Opening README documentation...
echo.
type README.md | more
echo.
pause
goto menu

:exit
echo.
echo Thanks for using UOWD Aerospace Machine Vision System!
echo.
pause
exit
