@echo off
title RAG Backend Server
echo ========================================
echo  RAG Backend Server
echo ========================================
echo.

:: Check if we're in the right directory
if not exist "backend" (
    echo Error: backend directory not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

cd backend

echo Checking if virtual environment exists...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error creating virtual environment. Please check your Python installation.
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo Error activating virtual environment.
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r ..\requirements.txt
if errorlevel 1 (
    echo Error with main requirements.txt, trying minimal requirements...
    pip install -r ..\requirements-minimal.txt
    if errorlevel 1 (
        echo Error installing dependencies.
        pause
        exit /b 1
    )
)

echo.
echo Checking if .env file exists...
if not exist ".env" (
    echo Warning: .env file not found. Creating from template...
    if exist ".env.example" (
        copy .env.example .env
    )
    echo.
    echo IMPORTANT: Please edit backend\.env and add your API keys!
    echo The file has been created from the template.
    echo.
    pause
)

echo.
echo Starting FastAPI server...
echo Backend will be available at: http://localhost:8000
echo API Documentation will be available at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
