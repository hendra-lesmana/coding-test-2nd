import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Google Gemini API configuration
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")

    # Vector database configuration
    vector_db_path: str = os.getenv("VECTOR_DB_PATH", "./vector_store")
    vector_db_type: str = os.getenv("VECTOR_DB_TYPE", "chromadb")

    # PDF upload path
    pdf_upload_path: str = os.getenv("PDF_UPLOAD_PATH", "../data")

    # Embedding model configuration
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "models/embedding-001")

    # LLM configuration
    llm_model: str = os.getenv("LLM_MODEL", "gemini-1.5-flash")
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.1"))
    max_tokens: int = int(os.getenv("MAX_TOKENS", "1000"))

    # Chunking configuration
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))

    # Retrieval configuration
    retrieval_k: int = int(os.getenv("RETRIEVAL_K", "5"))
    similarity_threshold: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))

    # Server configuration
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"

    # CORS configuration
    allowed_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Logging configuration
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    def validate_settings(self):
        """Validate critical settings"""
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY is required. Please set it in the .env file.")

    class Config:
        env_file = ".env"


settings = Settings() 