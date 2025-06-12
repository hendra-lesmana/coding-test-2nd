@echo off
echo Starting RAG-based Financial Q&A System Backend...
echo.

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
        echo Error installing dependencies. Please run install_dependencies.bat instead.
        pause
        exit /b 1
    )
)

echo.
echo Checking if .env file exists...
if not exist ".env" (
    echo Warning: .env file not found. Creating from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit backend\.env and add your OpenAI API key!
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
