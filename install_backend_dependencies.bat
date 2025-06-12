@echo off
title Install Backend Dependencies - RAG Financial Q&A System
echo ========================================
echo  Installing Backend Dependencies
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

echo Installing Python dependencies for RAG Financial Q&A System...
echo.

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

echo Installing Python packages...
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

echo.
echo ========================================
echo  BACKEND INSTALLATION COMPLETE!
echo ========================================
echo.
echo ✓ Python virtual environment ready
echo ✓ All Python dependencies installed
echo ✓ Configuration file created
echo.
echo NEXT STEPS:
echo 1. Edit backend\.env and add your API keys
echo 2. Install frontend dependencies: install_frontend_dependencies.bat
echo 3. Or install all at once: install_all_dependencies.bat
echo 4. Run backend: start_backend_only.bat
echo.
pause
