@echo off
title Install All Dependencies - RAG Financial Q&A System
echo ========================================
echo  Installing All Dependencies
echo  RAG Financial Q&A System
echo ========================================
echo.

:: Check if we're in the right directory
if not exist "backend" (
    echo Error: backend directory not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

if not exist "frontend" (
    echo Error: frontend directory not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

echo This script will install dependencies for both backend and frontend.
echo.
echo Requirements:
echo - Python 3.8+ installed and in PATH
echo - Node.js 16+ installed and in PATH
echo.
pause

echo ========================================
echo  STEP 1: Installing Backend Dependencies
echo ========================================
echo.

cd backend

echo Checking if virtual environment exists...
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error creating virtual environment.
        echo Please ensure Python 3.8+ is installed and in your PATH.
        echo Download from: https://python.org
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created successfully
) else (
    echo ✓ Virtual environment already exists
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo Error activating virtual environment.
    pause
    exit /b 1
)

echo ✓ Virtual environment activated
echo.

echo Installing Python dependencies...
echo Trying main requirements.txt...
pip install -r ..\requirements.txt
if errorlevel 1 (
    echo Main requirements failed, trying minimal requirements...
    pip install -r ..\requirements-minimal.txt
    if errorlevel 1 (
        echo Error installing Python dependencies.
        echo Please check your internet connection and Python installation.
        pause
        exit /b 1
    )
    echo ✓ Minimal Python dependencies installed
) else (
    echo ✓ Full Python dependencies installed
)

echo.
echo Checking if .env file exists...
if not exist ".env" (
    echo Creating .env file from template...
    if exist ".env.example" (
        copy .env.example .env
        echo ✓ .env file created from template
    ) else (
        echo # RAG Financial Q&A System Configuration > .env
        echo. >> .env
        echo # Choose one of the following API keys: >> .env
        echo GEMINI_API_KEY=your_gemini_api_key_here >> .env
        echo # OPENAI_API_KEY=your_openai_api_key_here >> .env
        echo. >> .env
        echo # Vector Store Configuration >> .env
        echo VECTOR_STORE_PATH=./vector_store >> .env
        echo ✓ .env file created with template
    )
    echo.
    echo IMPORTANT: Please edit backend\.env and add your API keys!
    echo.
) else (
    echo ✓ .env file already exists
)

cd ..

echo.
echo ========================================
echo  STEP 2: Installing Frontend Dependencies
echo ========================================
echo.

cd frontend

echo Installing Node.js dependencies...
npm install
if errorlevel 1 (
    echo Error installing Node.js dependencies.
    echo Please ensure Node.js 16+ is installed and in your PATH.
    echo Download from: https://nodejs.org
    pause
    exit /b 1
)

echo ✓ Node.js dependencies installed successfully

cd ..

echo.
echo ========================================
echo  INSTALLATION COMPLETE!
echo ========================================
echo.
echo ✓ Backend dependencies installed (Python virtual environment)
echo ✓ Frontend dependencies installed (Node.js packages)
echo ✓ Configuration files created
echo.
echo NEXT STEPS:
echo 1. Edit backend\.env and add your API keys:
echo    - Get Gemini API key: https://makersuite.google.com/app/apikey
echo    - Or get OpenAI API key: https://platform.openai.com/api-keys
echo.
echo 2. Run the application:
echo    - Windows: start_app.bat
echo    - Or run services individually:
echo      * Backend: start_backend_only.bat
echo      * Frontend: start_frontend_only.bat
echo.
echo 3. Access the application:
echo    - Frontend: http://localhost:3000
echo    - Backend API: http://localhost:8000
echo    - API Docs: http://localhost:8000/docs
echo.
pause
