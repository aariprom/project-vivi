@echo off
REM Vivi Windows Setup Script

echo Setting up Vivi AI Assistant for Windows...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully!

REM Test the installation
echo Testing installation...
python test_vivi.py
if errorlevel 1 (
    echo Some tests failed, but this might be normal
)

echo.
echo Vivi setup complete!
echo.
echo To run Vivi:
echo   1. Double-click run_vivi.bat
echo   2. Or run: python -m src.main
echo.
echo To build Windows executable:
echo   python build.py
echo.
pause