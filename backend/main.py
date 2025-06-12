from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models.schemas import ChatRequest, ChatResponse, DocumentsResponse, UploadResponse
from services.pdf_processor import PDFProcessor
from services.vector_store import VectorStoreService
from services.rag_pipeline import RAGPipeline
from config import settings
import logging
import time
import os
import aiofiles

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG-based Financial Statement Q&A System",
    description="AI-powered Q&A system for financial documents using RAG",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
pdf_processor = None
vector_store = None
rag_pipeline = None


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global pdf_processor, vector_store, rag_pipeline

    try:
        logger.info("Starting RAG Q&A System...")

        # Validate settings first
        settings.validate_settings()
        logger.info("Settings validated successfully")

        # Initialize PDF processor
        pdf_processor = PDFProcessor()
        logger.info("PDF processor initialized")

        # Initialize vector store
        vector_store = VectorStoreService()
        logger.info("Vector store initialized")

        # Initialize RAG pipeline
        rag_pipeline = RAGPipeline(vector_store)
        logger.info("RAG pipeline initialized")

        logger.info("All services initialized successfully")

    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        logger.error("Please check your configuration and ensure all required environment variables are set.")
        raise


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "RAG-based Financial Statement Q&A System is running"}


@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process PDF file"""
    start_time = time.time()

    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        if not file.content_type == 'application/pdf':
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file")

        # Ensure upload directory exists
        upload_dir = settings.pdf_upload_path
        os.makedirs(upload_dir, exist_ok=True)

        # Save uploaded file
        file_path = os.path.join(upload_dir, file.filename)

        # Read and save file content
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        logger.info(f"File saved to: {file_path}")

        # Process PDF and extract documents
        documents = pdf_processor.process_pdf(file_path)

        if not documents:
            raise HTTPException(status_code=400, detail="No text content could be extracted from the PDF")

        # Store documents in vector database
        vector_store.add_documents(documents)

        processing_time = time.time() - start_time

        logger.info(f"Successfully processed {file.filename}: {len(documents)} chunks in {processing_time:.2f}s")

        return UploadResponse(
            message="PDF uploaded and processed successfully",
            filename=file.filename,
            chunks_count=len(documents),
            processing_time=processing_time
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Process chat request and return AI response"""
    try:
        # Validate request
        if not request.question or not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        # Check if vector store has documents
        doc_count = vector_store.get_document_count()
        if doc_count == 0:
            raise HTTPException(
                status_code=400,
                detail="No documents have been uploaded yet. Please upload a PDF document first."
            )

        logger.info(f"Processing chat request: '{request.question[:100]}...'")

        # Use RAG pipeline to generate answer
        result = rag_pipeline.generate_answer(
            question=request.question,
            chat_history=request.chat_history
        )

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            processing_time=result["processing_time"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


@app.get("/api/documents")
async def get_documents():
    """Get list of processed documents"""
    try:
        # Get document count from vector store
        doc_count = vector_store.get_document_count()

        # For now, we'll return basic info about processed documents
        # In a production system, you might want to store document metadata separately
        documents = []

        # Check if there are any uploaded files
        upload_dir = settings.pdf_upload_path
        if os.path.exists(upload_dir):
            for filename in os.listdir(upload_dir):
                if filename.lower().endswith('.pdf'):
                    file_path = os.path.join(upload_dir, filename)
                    file_stat = os.stat(file_path)

                    documents.append({
                        "filename": filename,
                        "upload_date": time.ctime(file_stat.st_mtime),
                        "chunks_count": doc_count,  # This is approximate
                        "status": "processed" if doc_count > 0 else "pending"
                    })

        return DocumentsResponse(documents=documents)

    except Exception as e:
        logger.error(f"Error getting documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving documents: {str(e)}")


@app.get("/api/chunks")
async def get_chunks():
    """Get document chunks (optional endpoint)"""
    try:
        # This is a simplified implementation
        # In a production system, you might want to implement pagination
        doc_count = vector_store.get_document_count()

        # Return basic chunk information
        return {
            "total_chunks": doc_count,
            "message": f"Vector store contains {doc_count} document chunks"
        }

    except Exception as e:
        logger.error(f"Error getting chunks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving chunks: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port, reload=settings.debug) 