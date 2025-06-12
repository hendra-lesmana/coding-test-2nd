@echo off
title RAG Financial Q&A System
echo ========================================
echo  RAG-based Financial Q&A System
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

echo Starting both Backend and Frontend...
echo.
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:3000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C in either window to stop the servers
echo.

:: Start backend in a new window
echo Starting Backend...
start "RAG Backend" cmd /k "cd backend && call venv\Scripts\activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

:: Wait a moment for backend to start
timeout /t 3 /nobreak >nul

:: Start frontend in a new window
echo Starting Frontend...
start "RAG Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Both services are starting in separate windows...
echo.
echo To stop the application:
echo 1. Close both terminal windows, or
echo 2. Press Ctrl+C in each window
echo.

:: Wait for user input before closing this window
echo Press any key to open the application in your browser...
pause >nul

:: Open the application in default browser
start http://localhost:3000

echo.
echo Application opened in browser!
echo Keep the backend and frontend terminal windows open.
echo.
pause
