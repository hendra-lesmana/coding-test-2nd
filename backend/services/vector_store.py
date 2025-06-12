from typing import List, Tuple, Optional
from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import settings
import logging
import os
import chromadb
from chromadb.config import Settings as ChromaSettings

logger = logging.getLogger(__name__)


class VectorStoreService:
    def __init__(self):
        """Initialize vector store with ChromaDB and embeddings"""
        try:
            # Try to initialize Google Gemini embeddings first, fallback to local embeddings
            try:
                if settings.google_api_key and settings.google_api_key.strip():
                    self.embeddings = GoogleGenerativeAIEmbeddings(
                        model=settings.embedding_model,
                        google_api_key=settings.google_api_key
                    )
                    logger.info("Using Google Gemini embeddings")
                else:
                    raise ValueError("No Google API key provided")
            except Exception as e:
                logger.warning(f"Google Gemini embeddings failed: {str(e)}, falling back to local embeddings")
                # Fallback to local HuggingFace embeddings
                self.embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={'device': 'cpu'}
                )
                logger.info("Using local HuggingFace embeddings (sentence-transformers/all-MiniLM-L6-v2)")

            # Ensure vector store directory exists
            os.makedirs(settings.vector_db_path, exist_ok=True)

            # Initialize ChromaDB client
            self.chroma_client = chromadb.PersistentClient(
                path=settings.vector_db_path,
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )

            # Initialize or get collection
            self.collection_name = "financial_documents"
            try:
                self.collection = self.chroma_client.get_collection(self.collection_name)
                logger.info(f"Loaded existing collection: {self.collection_name}")
            except:
                self.collection = self.chroma_client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "Financial statement documents"}
                )
                logger.info(f"Created new collection: {self.collection_name}")

            # Initialize Langchain Chroma wrapper
            self.vector_store = Chroma(
                client=self.chroma_client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings
            )

            logger.info("VectorStoreService initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing VectorStoreService: {str(e)}")
            raise

    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store"""
        try:
            if not documents:
                logger.warning("No documents to add")
                return

            logger.info(f"Adding {len(documents)} documents to vector store")

            # Add documents to the vector store
            self.vector_store.add_documents(documents)

            logger.info(f"Successfully added {len(documents)} documents to vector store")

        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise

    def similarity_search(self, query: str, k: int = None) -> List[Tuple[Document, float]]:
        """Search for similar documents"""
        try:
            if k is None:
                k = settings.retrieval_k

            logger.info(f"Searching for similar documents with query: '{query[:100]}...' (k={k})")

            # Perform similarity search with scores
            results = self.vector_store.similarity_search_with_score(query, k=k)

            # Filter by similarity threshold
            filtered_results = [
                (doc, score) for doc, score in results
                if score >= settings.similarity_threshold
            ]

            logger.info(f"Found {len(filtered_results)} documents above similarity threshold")
            return filtered_results

        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            raise

    def delete_documents(self, document_ids: List[str]) -> None:
        """Delete documents from vector store"""
        try:
            if not document_ids:
                logger.warning("No document IDs provided for deletion")
                return

            logger.info(f"Deleting {len(document_ids)} documents from vector store")

            # Delete documents by IDs
            self.collection.delete(ids=document_ids)

            logger.info(f"Successfully deleted {len(document_ids)} documents")

        except Exception as e:
            logger.error(f"Error deleting documents: {str(e)}")
            raise

    def get_document_count(self) -> int:
        """Get total number of documents in vector store"""
        try:
            count = self.collection.count()
            logger.info(f"Vector store contains {count} documents")
            return count

        except Exception as e:
            logger.error(f"Error getting document count: {str(e)}")
            return 0

    def clear_collection(self) -> None:
        """Clear all documents from the collection"""
        try:
            logger.info("Clearing all documents from vector store")
            self.chroma_client.delete_collection(self.collection_name)
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"description": "Financial statement documents"}
            )
            # Reinitialize the vector store
            self.vector_store = Chroma(
                client=self.chroma_client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings
            )
            logger.info("Successfully cleared vector store")

        except Exception as e:
            logger.error(f"Error clearing vector store: {str(e)}")
            raise