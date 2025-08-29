@echo off
echo UOWD Aerospace Machine Vision - Installation Script
echo ===================================================

echo.
echo Installing Python dependencies...
echo.

pip install opencv-python==4.8.1.78
if %errorlevel% neq 0 (
    echo Failed to install OpenCV
    pause
    exit /b 1
)

pip install numpy==1.24.3
if %errorlevel% neq 0 (
    echo Failed to install NumPy
    pause
    exit /b 1
)

pip install pillow==10.0.1
if %errorlevel% neq 0 (
    echo Failed to install Pillow
    pause
    exit /b 1
)

echo.
echo ===================================================
echo Installation completed successfully!
echo ===================================================
echo.
echo You can now run:
echo   python test_system.py        - Test the system
echo   python machine_vision.py     - Basic version
echo   python advanced_machine_vision.py - Advanced version
echo.
echo Press any key to run system test...
pause > nul

python test_system.py

pause
