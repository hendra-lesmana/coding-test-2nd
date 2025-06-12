# 📋 Scripts Overview - RAG Financial Q&A System

This document provides a complete overview of all available scripts for the RAG Financial Q&A System.

## 🚀 Quick Reference

### **For First-Time Setup:**
1. **Windows**: Run `install_all_dependencies.bat` then `start_app.bat`
2. **Unix/Linux/macOS**: Run `./install_all_dependencies.sh` then `./start_app.sh`

### **For Daily Development:**
1. **Windows**: Just run `start_app.bat`
2. **Unix/Linux/macOS**: Just run `./start_app.sh`

---

## 📦 Dependency Installation Scripts

### **Complete Installation**
| Script | Platform | Purpose |
|--------|----------|---------|
| `install_all_dependencies.bat` | Windows | Installs all backend + frontend dependencies |
| `install_all_dependencies.sh` | Unix/Linux/macOS | Installs all backend + frontend dependencies |

**What they do:**
- ✅ Create Python virtual environment
- ✅ Install all Python packages (FastAPI, uvicorn, etc.)
- ✅ Install all Node.js packages (Next.js, React, etc.)
- ✅ Create configuration files (.env)
- ✅ Validate installations
- ✅ Show next steps

### **Individual Installation**
| Script | Platform | Purpose |
|--------|----------|---------|
| `install_backend_dependencies.bat` | Windows | Backend Python dependencies only |
| `install_backend_dependencies.sh` | Unix/Linux/macOS | Backend Python dependencies only |
| `install_frontend_dependencies.bat` | Windows | Frontend Node.js dependencies only |
| `install_frontend_dependencies.sh` | Unix/Linux/macOS | Frontend Node.js dependencies only |

---

## 🎯 Application Startup Scripts

### **Complete Application**
| Script | Platform | Purpose |
|--------|----------|---------|
| `start_app.bat` | Windows | Starts both backend + frontend (recommended) |
| `start_app.sh` | Unix/Linux/macOS | Starts both backend + frontend (recommended) |

**What they do:**
- ✅ Auto-install dependencies if needed
- ✅ Start FastAPI backend server (port 8000)
- ✅ Start Next.js frontend server (port 3000)
- ✅ Open browser automatically
- ✅ Handle process management

### **Individual Services**
| Script | Platform | Purpose |
|--------|----------|---------|
| `start_backend_only.bat` | Windows | Backend FastAPI server only |
| `start_backend_only.sh` | Unix/Linux/macOS | Backend FastAPI server only |
| `start_frontend_only.bat` | Windows | Frontend Next.js server only |
| `start_frontend_only.sh` | Unix/Linux/macOS | Frontend Next.js server only |

---

## 🔧 Legacy Scripts (Already Existed)

| Script | Platform | Purpose |
|--------|----------|---------|
| `install_dependencies.bat` | Windows | Original dependency installer |
| `start_backend.bat` | Windows | Original backend starter |
| `start_frontend.bat` | Windows | Original frontend starter |

---

## 🌐 Access Points After Starting

| Service | URL | Description |
|---------|-----|-------------|
| **Main Application** | http://localhost:3000 | Compact dark theme UI |
| **Backend API** | http://localhost:8000 | FastAPI server |
| **API Documentation** | http://localhost:8000/docs | Interactive API docs |

---

## 📝 Usage Examples

### **Complete Setup (First Time)**
```bash
# Windows
git clone <repo-url>
cd coding-test-2nd
install_all_dependencies.bat
start_app.bat

# Unix/Linux/macOS
git clone <repo-url>
cd coding-test-2nd
chmod +x *.sh
./install_all_dependencies.sh
./start_app.sh
```

### **Daily Development**
```bash
# Windows
start_app.bat

# Unix/Linux/macOS
./start_app.sh
```

### **Backend Development Only**
```bash
# Windows
start_backend_only.bat

# Unix/Linux/macOS
./start_backend_only.sh
```

### **Frontend Development Only**
```bash
# Windows
start_frontend_only.bat

# Unix/Linux/macOS
./start_frontend_only.sh
```

---

## 🛑 Stopping Services

### **Windows**
- Close the terminal windows
- Or press `Ctrl+C` in each terminal

### **Unix/Linux/macOS**
- Press `Ctrl+C` in the terminal (stops both services)

---

## ⚙️ Configuration

### **Required Setup**
1. **API Keys**: Edit `backend/.env`:
   ```env
   GEMINI_API_KEY=your_key_here
   # OR
   OPENAI_API_KEY=your_key_here
   ```

2. **Get API Keys**:
   - **Gemini**: https://makersuite.google.com/app/apikey
   - **OpenAI**: https://platform.openai.com/api-keys

### **Requirements**
- **Python 3.8+** (for backend)
- **Node.js 16+** (for frontend)
- **Internet connection** (for dependency installation)

---

## 🎉 Success Indicators

When everything is working correctly:
- ✅ Backend server running on port 8000
- ✅ Frontend server running on port 3000
- ✅ Browser opens automatically to the application
- ✅ Compact dark theme interface loads
- ✅ No error messages in terminals

---

## 📞 Need Help?

1. **Check troubleshooting** in README.md
2. **Verify requirements** (Python 3.8+, Node.js 16+)
3. **Check API keys** in backend/.env
4. **Try individual scripts** to isolate issues
5. **Run dependency installers** separately if needed
