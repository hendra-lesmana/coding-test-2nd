# Troubleshooting Guide

## Installation Issues

### 1. Unicode Decode Error (Fixed)
**Error**: `UnicodeDecodeError: 'charmap' codec can't decode byte`

**Solution**: This has been fixed by removing Korean comments from requirements.txt. Try again with the updated files.

### 2. Dependency Installation Failures

**Option A**: Use the step-by-step installer
```bash
install_dependencies.bat
```

**Option B**: Install manually
```bash
cd backend
venv\Scripts\activate
pip install --upgrade pip
pip install fastapi uvicorn[standard] python-multipart
pip install PyPDF2 pdfplumber
pip install openai langchain langchain-openai langchain-community
pip install chromadb sentence-transformers
pip install numpy python-dotenv pydantic pydantic-settings requests aiofiles
```

**Option C**: Use minimal requirements
```bash
pip install -r requirements-minimal.txt
```

### 3. Python Version Issues
- Ensure you have Python 3.8 or higher
- Check with: `python --version`
- If using conda: `conda create -n rag-qa python=3.10`

### 4. Virtual Environment Issues
```bash
# Delete existing venv and recreate
rmdir /s backend\venv
cd backend
python -m venv venv
venv\Scripts\activate
```

## Runtime Issues

### 1. OpenAI API Key Error
**Error**: `OPENAI_API_KEY is required`

**Solution**:
1. Get API key from https://platform.openai.com/api-keys
2. Edit `backend\.env`
3. Set: `OPENAI_API_KEY=your_actual_key_here`

### 2. Port Already in Use
**Error**: `Address already in use`

**Solution**:
- Change port in `backend\.env`: `PORT=8001`
- Or kill existing process: `taskkill /f /im python.exe`

### 3. CORS Errors
**Error**: `Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Solution**: Backend should handle this automatically. If not, check `ALLOWED_ORIGINS` in `backend\.env`

### 4. Module Import Errors
**Error**: `ModuleNotFoundError: No module named 'langchain'`

**Solution**:
1. Ensure virtual environment is activated
2. Reinstall dependencies: `pip install -r requirements.txt`

## Frontend Issues

### 1. Node.js Dependencies
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### 2. Tailwind CSS Not Working
```bash
cd frontend
npm install tailwindcss autoprefixer postcss
npm run dev
```

### 3. TypeScript Errors
- Ensure all dependencies are installed
- Restart VS Code
- Run: `npm run build` to check for errors

## Performance Issues

### 1. Slow PDF Processing
- Normal for first upload (model loading)
- Subsequent uploads should be faster
- Consider smaller chunk sizes in `backend\.env`

### 2. Slow Chat Responses
- First response is slower (cold start)
- Check OpenAI API status
- Consider using `gpt-3.5-turbo` instead of `gpt-4`

## Testing the Setup

### Quick Test
```bash
python test_setup.py
```

### Manual Testing
1. Backend health: http://localhost:8000
2. API docs: http://localhost:8000/docs
3. Frontend: http://localhost:3000

### Test API Endpoints
```bash
# Test upload (replace with actual PDF path)
curl -X POST "http://localhost:8000/api/upload" -F "file=@data/sample.pdf"

# Test documents
curl "http://localhost:8000/api/documents"

# Test chat
curl -X POST "http://localhost:8000/api/chat" -H "Content-Type: application/json" -d '{"question": "What is this document about?"}'
```

## Common Solutions

### Reset Everything
```bash
# Backend
cd backend
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r ..\requirements-minimal.txt

# Frontend
cd frontend
rmdir /s node_modules
del package-lock.json
npm install
```

### Check Logs
- Backend logs appear in the terminal where you ran the server
- Frontend logs appear in browser console (F12)
- Check for specific error messages

### Environment Variables
Ensure your `backend\.env` file contains:
```
OPENAI_API_KEY=your_key_here
VECTOR_DB_PATH=./vector_store
PDF_UPLOAD_PATH=../data
LLM_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-ada-002
```

## Getting Help

1. Check error messages carefully
2. Try the solutions above
3. Ensure all prerequisites are installed
4. Check that your OpenAI API key is valid and has credits
5. Try with a simple PDF file first

If issues persist, provide:
- Error message (full traceback)
- Python version (`python --version`)
- Node.js version (`node --version`)
- Operating system
- Steps you've tried
