@echo off
REM Vivi Windows Run Script

echo Starting Vivi AI Assistant...

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found!
    echo Please run setup_vivi.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if we're in the right directory
if not exist "src\main.py" (
    echo Vivi source files not found!
    echo Please run this script from the Vivi project directory
    pause
    exit /b 1
)

echo Environment ready
echo Launching Vivi...
echo.

REM Run the application
python -m src.main

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Vivi encountered an error
    pause
)