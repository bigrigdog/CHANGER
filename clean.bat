@echo off

REM Function to check if a command was successful
:check_error
if %errorlevel% neq 0 (
    echo Error: %1 failed.
    pause
    exit /b 1
)

REM Function to prompt user for input
:get_input
set /p PROJECT_DIR="Enter the project directory path: "
if not exist "%PROJECT_DIR%" (
    echo Error: Project directory does not exist.
    pause
    exit /b 1
)

REM Set project directory
echo Setting project directory...
cd /d "%PROJECT_DIR%"

REM Set up Sphinx documentation
echo Setting up Sphinx Documentation...
sphinx-quickstart > nul
call :check_error sphinx-quickstart

REM Install autopep8 and pylint
echo Installing autopep8 and pylint...
pip install autopep8 pylint > nul
call :check_error "pip install autopep8 pylint"

REM Setting up GitHub Actions Workflow
echo Setting up GitHub Actions Workflow...
mkdir "%PROJECT_DIR%\.github\workflows"
echo @echo off > "%PROJECT_DIR%\.github\workflows\main.yml"

echo Done!
pause
