# RAG-based Financial Statement Q&A System Coding Challenge

## Overview
Build a full-stack application using **RAG (Retrieval Augmented Generation)** technology:
1. **Next.js** as the frontend framework with **compact dark theme UI**
2. **FastAPI** as the backend API layer
3. **PDF financial statement document** based intelligent Q&A system
4. **Vector database** for document search and generative AI

Parse and embed the provided **`FinancialStatement_2025_I_AADIpdf.pdf`** file, then build a system where users can ask questions about the financial statement and AI generates answers by retrieving relevant information.

✨ **Features a modern, compact dark theme interface with no scrolling** - everything fits in a single screen view for optimal user experience.

---

## How to Complete This Assignment

### 📋 **Assignment Process**
1. **Fork this repository** to your own GitHub account
2. **Clone your forked repository** to your local machine
3. **Complete the coding challenge** following the requirements below
4. **Push your completed solution** to your forked repository
5. **Send your repository URL via email** when completed

### 🚀 **Getting Started**
```bash
# Fork this repository on GitHub (click "Fork" button)
# Then clone your forked repository
git clone https://github.com/YOUR_USERNAME/coding-test-2nd.git
cd coding-test-2nd

# Start development...
```

### ✉️ **Submission**
When you complete the assignment:
- Ensure your code is pushed to your forked repository
- Test that your application runs correctly
- **Send your GitHub repository URL via email**
- Include any additional setup instructions if needed

---

## Requirements

### 1. **PDF Document Processing & RAG Pipeline (Required)**
   - Parse PDF file to text and split into chunks
   - Convert each chunk to vector embeddings and store in vector database
   - Implement retrieval system that embeds user questions and searches for relevant document chunks
   - Implement generation system that combines retrieved context with questions and sends to LLM

### 2. **Backend API (Required)**
   - Implement the following endpoints using **FastAPI**:
     - `POST /api/upload`: PDF file upload and vectorization processing
     - `GET /api/documents`: Retrieve processed document information
     - `POST /api/chat`: Generate RAG-based answers to questions
     - `GET /api/chunks`: Retrieve document chunks and metadata (optional)
   - Configure CORS to allow API calls from Next.js app
   - Integrate with vector database (e.g., Chroma, FAISS, Pinecone, etc.)

### 3. **Frontend UI/UX (Required)**
   - Implement user-friendly chat interface using **Next.js**
   - Real-time Q&A functionality (chat format)
   - Document upload status display and processing progress
   - Display referenced document chunk sources with answers
   - Loading states and error handling

### 4. **Recommended Tech Stack**
   - **Document Processing**: PyPDF2, pdfplumber, or langchain Document Loaders
   - **Embedding Models**: Google Gemini embeddings, Sentence Transformers, or HuggingFace embeddings
   - **Vector Database**: ChromaDB (local), FAISS, or Pinecone
   - **LLM**: Google Gemini (default), OpenAI GPT, Anthropic Claude, or open-source models
   - **Frameworks**: LangChain or LlamaIndex (for RAG pipeline construction)

### 5. **Bonus Features (Optional)**
   - Multi-PDF file support
   - Conversation history maintenance and context continuity
   - Answer quality evaluation and feedback system
   - Visual highlighting of document chunks
   - Financial metrics calculator integration
   - Chart and graph generation functionality

---

## Free LLM APIs and Embedding Services

### LLM Services
- **Google Gemini API**: Free tier available (recommended)
- **OpenAI API**: GPT-3.5/4 (requires payment)
- **Anthropic Claude**: Free credits provided
- **Cohere**: Free API available
- **Hugging Face**: Free open-source models

### Embedding Services
- **Google Gemini Embeddings**: models/embedding-001 (free tier)
- **Sentence Transformers**: Open-source models for local execution
- **OpenAI Embeddings**: text-embedding-ada-002 (requires payment)
- **Hugging Face Embeddings**: Various free models available

### Vector Databases
- **ChromaDB**: Free local and cloud usage
- **FAISS**: Free open-source by Meta
- **Weaviate**: Free cloud tier available
- **Pinecone**: Free starter plan available

---

## Project Structure

```
coding-test-2nd/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models/              # Data models
│   │   └── schemas.py       # Pydantic schemas
│   ├── services/            # RAG service logic
│   │   ├── pdf_processor.py # PDF processing and chunking
│   │   ├── vector_store.py  # Vector database integration
│   │   └── rag_pipeline.py  # RAG pipeline
│   ├── requirements.txt     # Python dependencies
│   └── config.py           # Configuration file
├── frontend/
│   ├── pages/              # Next.js pages
│   │   ├── index.tsx       # Main page
│   │   └── _app.tsx        # App component
│   ├── components/         # React components
│   │   ├── ChatInterface.tsx
│   │   └── FileUpload.tsx
│   ├── styles/             # CSS files
│   │   └── globals.css     # Global styles
│   ├── package.json        # Node.js dependencies
│   ├── tsconfig.json       # TypeScript configuration
│   ├── next.config.js      # Next.js configuration
│   ├── next-env.d.ts       # Next.js type definitions
│   └── .eslintrc.json      # ESLint configuration
├── data/
│   └── FinancialStatement_2025_I_AADIpdf.pdf
└── README.md
```

---

## Getting Started

### 🚀 **Quick Start (Recommended)**

The easiest way to run the application is using the provided scripts:

#### **Option 1: One-Command Setup (Easiest)**

**Windows Users:**
```bash
# Clone repository
git clone <your-repository-url>
cd coding-test-2nd

# Install dependencies and run the application
install_all_dependencies.bat
# Then run:
start_app.bat
```

**Unix/Linux/macOS Users:**
```bash
# Clone repository
git clone <your-repository-url>
cd coding-test-2nd

# Make scripts executable
chmod +x *.sh

# Install dependencies and run the application
./install_all_dependencies.sh
# Then run:
./start_app.sh
```

#### **Option 2: Direct Run (Dependencies Auto-Installed)**

**Windows Users:**
```bash
# Clone and run directly (auto-installs dependencies)
git clone <your-repository-url>
cd coding-test-2nd
start_app.bat
```

**Unix/Linux/macOS Users:**
```bash
# Clone and run directly (auto-installs dependencies)
git clone <your-repository-url>
cd coding-test-2nd
chmod +x *.sh
./start_app.sh
```

The scripts will automatically:
- ✅ **Set up Python virtual environment**
- ✅ **Install all dependencies** (Python and Node.js)
- ✅ **Create configuration files** (.env setup)
- ✅ **Start both services** (backend and frontend)
- ✅ **Open browser** automatically to http://localhost:3000

### 📋 **Available Scripts**

#### **Dependency Installation Scripts**
| Script | Purpose | Platform |
|--------|---------|----------|
| `install_all_dependencies.bat` / `install_all_dependencies.sh` | **Install all dependencies** - Backend + Frontend | Windows / Unix |
| `install_backend_dependencies.bat` / `install_backend_dependencies.sh` | Install backend dependencies only | Windows / Unix |
| `install_frontend_dependencies.bat` / `install_frontend_dependencies.sh` | Install frontend dependencies only | Windows / Unix |

#### **Application Startup Scripts**
| Script | Purpose | Platform |
|--------|---------|----------|
| `start_app.bat` / `start_app.sh` | **Main script** - Starts both services | Windows / Unix |
| `start_backend_only.bat` / `start_backend_only.sh` | Backend only | Windows / Unix |
| `start_frontend_only.bat` / `start_frontend_only.sh` | Frontend only | Windows / Unix |

### 🔧 **Dependency Installation (Separate Step)**

If you prefer to install dependencies separately before running the application:

#### **Install All Dependencies**
**Windows:**
```bash
install_all_dependencies.bat
```

**Unix/Linux/macOS:**
```bash
./install_all_dependencies.sh
```

#### **Install Individual Dependencies**
**Backend Only:**
```bash
# Windows
install_backend_dependencies.bat

# Unix/Linux/macOS
./install_backend_dependencies.sh
```

**Frontend Only:**
```bash
# Windows
install_frontend_dependencies.bat

# Unix/Linux/macOS
./install_frontend_dependencies.sh
```

### 🛠️ **What the Dependency Installation Scripts Do**

#### **Backend Dependencies (`install_backend_dependencies.*`)**
- ✅ **Creates Python virtual environment** (if not exists)
- ✅ **Activates virtual environment**
- ✅ **Installs Python packages** from requirements.txt
- ✅ **Creates .env configuration file** from template
- ✅ **Validates Python installation**

#### **Frontend Dependencies (`install_frontend_dependencies.*`)**
- ✅ **Validates Node.js and npm installation**
- ✅ **Installs all Node.js packages** (Next.js, React, TypeScript, etc.)
- ✅ **Verifies installation success**
- ✅ **Sets up development environment**

#### **All Dependencies (`install_all_dependencies.*`)**
- ✅ **Combines both backend and frontend installation**
- ✅ **Provides comprehensive setup in one command**
- ✅ **Includes error handling and validation**
- ✅ **Shows next steps after installation**

### ⚙️ **Configuration Required**

After installation, set up your API keys:

1. **Edit `backend/.env`** (created automatically by scripts):
   ```env
   # Choose one of the following:
   GEMINI_API_KEY=your_gemini_api_key_here
   # OR
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. **Get API Keys**:
   - **Google Gemini**: https://makersuite.google.com/app/apikey (Free tier available)
   - **OpenAI**: https://platform.openai.com/api-keys (Requires payment)

### 🌐 **Access Points**
After starting the application:
- **Frontend (Main App)**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 🎯 **Using the Application**
1. **Open** http://localhost:3000 in your browser (opens automatically)
2. **Upload** a PDF financial statement using the compact upload area
3. **Wait** for document processing (progress shown)
4. **Ask questions** about the financial data in the dark theme chat interface
5. **Get AI-powered answers** with source references

### 🛑 **Stopping the Application**
- **Windows**: Close the terminal windows or press Ctrl+C in each
- **Unix/Linux/macOS**: Press Ctrl+C in the terminal (stops both services)

---

### 🔧 **Manual Setup (Alternative)**

If you prefer manual setup or the scripts don't work:

#### **1. Environment Setup**
```bash
# Clone repository
git clone <your-repository-url>
cd coding-test-2nd

# Set up Python virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

#### **2. Backend Setup**
```bash
cd backend

# Install dependencies
pip install -r ../requirements.txt

# Set up environment variables
# Edit the .env file and add your API key
GEMINI_API_KEY=your_gemini_api_key_here

# Run server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### **3. Frontend Setup**
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

---

## API Endpoints

### **POST /api/upload**
Upload PDF file and store in vector database
```json
{
  "file": "multipart/form-data"
}
```

### **POST /api/chat**
Generate RAG-based answer to question
```json
{
  "question": "What is the total revenue for 2025?",
  "chat_history": [] // optional
}
```

Response:
```json
{
  "answer": "The total revenue for 2025 is 123.4 billion won...",
  "sources": [
    {
      "content": "Related document chunk content",
      "page": 1,
      "score": 0.85
    }
  ],
  "processing_time": 2.3
}
```

### **GET /api/documents**
Retrieve processed document information
```json
{
  "documents": [
    {
      "filename": "FinancialStatement_2025_I_AADIpdf.pdf",
      "upload_date": "2024-01-15T10:30:00Z",
      "chunks_count": 125,
      "status": "processed"
    }
  ]
}
```

---

## Evaluation Criteria

### 1. **RAG System Implementation (30%)**
   - PDF processing and chunking quality
   - Embedding and vector search accuracy
   - LLM integration and answer quality

### 2. **Code Quality & Structure (30%)**
   - Code readability and maintainability
   - Modularization and separation of concerns
   - Error handling and logging

### 3. **User Experience (20%)**
   - Intuitive chat interface
   - Real-time feedback and loading states
   - Answer source display and reliability

### 4. **Technical Implementation (20%)**
   - API design and documentation
   - Performance optimization
   - Scalable architecture

---

## Submission

### 📦 **What to Submit**
1. **Your forked GitHub repository** with complete implementation
2. **All source code** (frontend, backend, configurations)
3. **Updated documentation** with any additional setup instructions
4. **Runnable demo** that works locally

### 📧 **How to Submit**
1. **Complete your implementation** in your forked repository
2. **Test thoroughly** to ensure everything works
3. **Push all changes** to your GitHub repository
4. **Send an email** with your repository URL to the designated contact

### 📝 **Repository Should Include**
- Complete frontend and backend implementation
- All necessary configuration files
- Clear installation and execution instructions
- Any additional documentation or notes

### 🎥 **Optional Extras**
- **Demo video** showing your system in action
- **Performance analysis** or optimization notes
- **Future improvement suggestions**

---

## Sample Questions

Your system should be able to handle questions like these about the financial statement PDF:

- "What is the total revenue for 2025?"
- "What is the year-over-year operating profit growth rate?"
- "What are the main cost items?"
- "How is the cash flow situation?"
- "What is the debt ratio?"

---

## Troubleshooting

### Dependency Installation Issues

**Python not found during installation**:
```bash
# Windows: Install Python 3.8+ from python.org
# Make sure to check "Add Python to PATH" during installation

# Unix/Linux: Install Python 3.8+
sudo apt update && sudo apt install python3 python3-pip python3-venv  # Ubuntu/Debian
sudo yum install python3 python3-pip  # CentOS/RHEL
brew install python3  # macOS with Homebrew

# Verify installation:
python --version  # or python3 --version
```

**Node.js not found during installation**:
```bash
# Install Node.js 16+ from nodejs.org
# Or use package managers:

# Windows: Use installer from nodejs.org
# Unix/Linux:
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs  # Ubuntu/Debian

# macOS:
brew install node

# Verify installation:
node --version
npm --version
```

**Virtual environment creation fails**:
```bash
# Windows:
python -m pip install --upgrade pip
python -m pip install virtualenv

# Unix/Linux/macOS:
python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
```

**npm install fails**:
```bash
# Clear npm cache and try again:
npm cache clean --force
npm install

# If still failing, delete node_modules and try:
rm -rf node_modules package-lock.json  # Unix/Linux/macOS
rmdir /s node_modules & del package-lock.json  # Windows
npm install
```

### Startup Script Issues

**Scripts not working on Windows**:
```bash
# Try running from Command Prompt as Administrator
# Or use PowerShell:
powershell -ExecutionPolicy Bypass -File start_app.bat
```

**Permission denied on Unix/Linux/macOS**:
```bash
# Make scripts executable:
chmod +x *.sh

# If still having issues, run with bash:
bash start_app.sh
```

**Port already in use**:
```bash
# Kill processes on ports 3000 and 8000
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Unix/Linux/macOS:
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

**Python not found**:
- Install Python 3.8+ from [python.org](https://python.org)
- Ensure Python is in your system PATH
- Try `python3` instead of `python` on Unix systems

**Node.js not found**:
- Install Node.js 16+ from [nodejs.org](https://nodejs.org)
- Ensure npm is available in your PATH

### Common Application Issues

**API Key Errors**:
- Check that `backend/.env` file exists and contains valid API keys
- Verify API key format (no extra spaces or quotes)
- Test API key with the test scripts: `python test_gemini.py`

**Frontend TypeScript Errors**:
- Ensure `npm install` was completed successfully
- Check that `node_modules` directory exists and is populated
- Verify all configuration files are present

**Backend Import Errors**:
- Activate Python virtual environment
- Install all requirements: `pip install -r requirements.txt`
- Check Python path and module imports

**CORS Issues**:
- Ensure backend CORS settings allow frontend origin
- Check that API endpoints are accessible from frontend

**Document Upload Issues**:
- Ensure PDF file is less than 50MB
- Check that the backend vector store directory has write permissions
- Verify that the embedding service is working correctly

---

**Build a smarter document Q&A system with RAG technology!** 