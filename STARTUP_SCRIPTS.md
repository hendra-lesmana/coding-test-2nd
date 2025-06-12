# 🚀 Startup Scripts for RAG Financial Q&A System

This document explains how to use the startup scripts to run the RAG-based Financial Q&A System.

## 📁 Available Scripts

### Windows (.bat files)
- `start_app.bat` - **Recommended**: Starts both backend and frontend in separate windows
- `start_backend_only.bat` - Starts only the backend server
- `start_frontend_only.bat` - Starts only the frontend server

### Unix/Linux/macOS (.sh files)
- `start_app.sh` - **Recommended**: Starts both backend and frontend
- `start_backend_only.sh` - Starts only the backend server
- `start_frontend_only.sh` - Starts only the frontend server

## 🎯 Quick Start

### Windows Users
```bash
# Double-click or run from command prompt:
start_app.bat
```

### Unix/Linux/macOS Users
```bash
# Make executable (already done):
chmod +x *.sh

# Run the application:
./start_app.sh
```

## 🔧 What the Scripts Do

### Full Application (`start_app.*`)
1. **Checks dependencies** - Verifies project structure
2. **Sets up backend**:
   - Creates Python virtual environment (if needed)
   - Installs Python dependencies
   - Checks for .env configuration file
   - Starts FastAPI server on port 8000
3. **Sets up frontend**:
   - Installs Node.js dependencies
   - Starts Next.js development server on port 8000
4. **Opens browser** - Automatically opens http://localhost:3000
5. **Manages processes** - Handles cleanup when stopped

### Individual Services
- **Backend only**: Runs just the FastAPI server
- **Frontend only**: Runs just the Next.js development server

## 🌐 Access Points

After starting the application:

- **Frontend (Main App)**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## ⚙️ Configuration

### Required Setup
1. **API Keys**: Edit `backend/.env` with your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   # or
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. **Dependencies**: Scripts automatically install:
   - Python packages (FastAPI, uvicorn, etc.)
   - Node.js packages (Next.js, React, etc.)

## 🛑 Stopping the Application

### Windows
- Close the terminal windows, or
- Press `Ctrl+C` in each terminal window

### Unix/Linux/macOS
- Press `Ctrl+C` in the terminal (stops both services)

## 🔍 Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Kill processes on ports 3000 and 8000
   # Windows:
   netstat -ano | findstr :3000
   taskkill /PID <PID> /F
   
   # Unix/Linux/macOS:
   lsof -ti:3000 | xargs kill -9
   lsof -ti:8000 | xargs kill -9
   ```

2. **Python not found**:
   - Install Python 3.8+ from python.org
   - Ensure Python is in your PATH

3. **Node.js not found**:
   - Install Node.js 16+ from nodejs.org
   - Ensure npm is available

4. **Permission denied (Unix/Linux/macOS)**:
   ```bash
   chmod +x *.sh
   ```

### Script Features

- ✅ **Automatic dependency installation**
- ✅ **Environment setup**
- ✅ **Error handling and validation**
- ✅ **Cross-platform compatibility**
- ✅ **Colored output (Unix/Linux/macOS)**
- ✅ **Automatic browser opening**
- ✅ **Process management**

## 📝 Manual Alternative

If scripts don't work, you can start manually:

```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r ../requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

## 🎉 Success!

When everything is running correctly, you should see:
- Backend server at http://localhost:8000
- Frontend application at http://localhost:3000
- Automatic browser opening to the application

The compact dark theme interface will be ready for uploading PDFs and asking questions!
