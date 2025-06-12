@echo off
title Install Frontend Dependencies - RAG Financial Q&A System
echo ========================================
echo  Installing Frontend Dependencies
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

echo Installing Node.js dependencies for RAG Financial Q&A System...
echo.

echo Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js not found!
    echo Please install Node.js 16+ from: https://nodejs.org
    pause
    exit /b 1
)

npm --version >nul 2>&1
if errorlevel 1 (
    echo Error: npm not found!
    echo Please install Node.js 16+ from: https://nodejs.org
    pause
    exit /b 1
)

echo ✓ Node.js and npm are available
echo.

echo Installing Node.js packages...
npm install
if errorlevel 1 (
    echo Error installing Node.js dependencies.
    echo Please check your internet connection and Node.js installation.
    pause
    exit /b 1
)

echo ✓ Node.js dependencies installed successfully
echo.

echo Verifying installation...
if not exist "node_modules" (
    echo Error: node_modules directory not created.
    echo Installation may have failed.
    pause
    exit /b 1
)

echo ✓ Installation verified - node_modules directory exists
echo.

echo ========================================
echo  FRONTEND INSTALLATION COMPLETE!
echo ========================================
echo.
echo ✓ All Node.js dependencies installed
echo ✓ Next.js development environment ready
echo ✓ React and TypeScript configured
echo.
echo NEXT STEPS:
echo 1. Install backend dependencies: install_backend_dependencies.bat
echo 2. Or install all at once: install_all_dependencies.bat
echo 3. Run frontend: start_frontend_only.bat
echo 4. Run full application: start_app.bat
echo.
pause
