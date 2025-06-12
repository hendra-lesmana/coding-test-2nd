@echo off
echo Installing Python dependencies for RAG Q&A System...
echo.

cd backend

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing core dependencies...
pip install --upgrade pip

echo Installing FastAPI and web framework...
pip install fastapi uvicorn[standard] python-multipart

echo Installing PDF processing libraries...
pip install PyPDF2 pdfplumber

echo Installing AI and LangChain libraries...
pip install google-generativeai
pip install langchain langchain-google-genai langchain-community

echo Installing vector database...
pip install chromadb

echo Installing text processing...
pip install sentence-transformers

echo Installing utilities...
pip install numpy python-dotenv pydantic pydantic-settings requests aiofiles

echo Installing testing libraries...
pip install pytest pytest-asyncio httpx

echo.
echo Installation complete!
echo.
echo Next steps:
echo 1. Edit backend\.env and add your Google Gemini API key
echo 2. Run: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
echo.
pause
