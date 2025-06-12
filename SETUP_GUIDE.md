# RAG-based Financial Q&A System - Setup Guide

This guide will help you set up and run the RAG-based Financial Statement Q&A System.

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- OpenAI API key (get one from https://platform.openai.com/api-keys)

## Quick Start

### Step 1: Clone and Navigate
```bash
git clone <your-repository-url>
cd coding-test-2nd
```

### Step 2: Backend Setup

1. **Create Python Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   ```bash
   cd backend
   cp .env.example .env
   ```
   
   Edit the `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

4. **Start Backend Server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Step 3: Frontend Setup

1. **Open New Terminal and Navigate to Frontend**
   ```bash
   cd frontend
   ```

2. **Install Node.js Dependencies**
   ```bash
   npm install
   ```

3. **Start Frontend Development Server**
   ```bash
   npm run dev
   ```

### Step 4: Verify Setup

1. **Check if services are running:**
   - Backend: http://localhost:8000
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

2. **Run the test script (optional):**
   ```bash
   python test_setup.py
   ```

## Using the Application

1. **Open your browser** and go to http://localhost:3000

2. **Upload a PDF** financial statement using the drag-and-drop area

3. **Wait for processing** - the system will extract text and create embeddings

4. **Start asking questions** in the chat interface, such as:
   - "What is the total revenue for 2025?"
   - "What are the main cost items?"
   - "How is the cash flow situation?"

## Troubleshooting

### Backend Issues

**Error: "OPENAI_API_KEY is required"**
- Make sure you've set your OpenAI API key in `backend/.env`
- Verify the key is valid and has sufficient credits

**Error: "Module not found"**
- Ensure you've activated the virtual environment
- Run `pip install -r requirements.txt` again

**Port 8000 already in use**
- Change the port in `backend/.env`: `PORT=8001`
- Update the frontend API calls to use the new port

### Frontend Issues

**Error: "Cannot resolve module"**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

**Tailwind CSS not working**
- Ensure `tailwind.config.js` and `postcss.config.js` exist
- Restart the development server

**API calls failing**
- Verify the backend is running on http://localhost:8000
- Check browser console for CORS errors

### General Issues

**PDF upload fails**
- Ensure the PDF is not corrupted
- Check file size (max 50MB)
- Verify the backend has write permissions to the data directory

**Chat responses are slow**
- This is normal for the first request (cold start)
- Subsequent requests should be faster
- Consider using a faster OpenAI model like `gpt-3.5-turbo`

## Advanced Configuration

### Changing Models

Edit `backend/.env`:
```
LLM_MODEL=gpt-4  # For better quality (more expensive)
EMBEDDING_MODEL=text-embedding-ada-002  # Current default
```

### Adjusting Chunk Settings

Edit `backend/.env`:
```
CHUNK_SIZE=1500  # Larger chunks for more context
CHUNK_OVERLAP=300  # More overlap for better continuity
RETRIEVAL_K=3  # Fewer chunks for faster responses
```

### Using Different Vector Database

The system currently uses ChromaDB. To use FAISS:
```
VECTOR_DB_TYPE=faiss
```

## Development

### Adding New Features

1. **Backend**: Add new endpoints in `backend/main.py`
2. **Frontend**: Create new components in `frontend/components/`
3. **Services**: Extend functionality in `backend/services/`

### Running Tests

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## Production Deployment

For production deployment, consider:

1. **Environment Variables**: Use proper secret management
2. **Database**: Use a persistent vector database like Pinecone
3. **Scaling**: Use Docker containers and load balancers
4. **Security**: Add authentication and rate limiting
5. **Monitoring**: Add logging and error tracking

## Support

If you encounter issues:

1. Check the console logs for error messages
2. Verify all prerequisites are installed
3. Ensure your OpenAI API key is valid and has credits
4. Try the troubleshooting steps above

For additional help, check the main README.md file or create an issue in the repository.
