@echo off
title RAG Frontend Server
echo ========================================
echo  RAG Frontend Server
echo ========================================
echo.

:: Check if we're in the right directory
if not exist "frontend" (
    echo Error: frontend directory not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

cd frontend

echo Installing dependencies...
npm install
if errorlevel 1 (
    echo Error installing dependencies.
    pause
    exit /b 1
)

echo.
echo Starting Next.js development server...
echo Frontend will be available at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

npm run dev
