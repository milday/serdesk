@echo off
echo ================================================
echo ServiceDesk GUI Automation - Fixed Version
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import selenium, openpyxl, webdriver_manager, tkinter" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install selenium openpyxl webdriver-manager
    if errorlevel 1 (
        echo Error: Failed to install required packages
        pause
        exit /b 1
    )
)

REM Fix Excel formulas first
echo Fixing Excel formulas...
python fix_excel_formulas.py

REM Run the GUI
echo Starting GUI...
python servicedesk_gui_fixed.py

pause

