#!/usr/bin/env python3
"""
Test script to demonstrate source deduplication functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.rag_pipeline import RAGPipeline
from langchain.schema import Document
from config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_documents():
    """Create test documents with some duplicates"""
    documents = [
        # Similar content from same page (should be deduplicated)
        (Document(
            page_content="The company's total revenue for 2024 was $1.2 billion, representing a 15% increase from the previous year.",
            metadata={"page": 1, "source": "test.pdf", "chunk_id": "test_1_1"}
        ), 0.95),
        
        (Document(
            page_content="Total revenue for 2024 reached $1.2 billion, which is a 15% growth compared to 2023.",
            metadata={"page": 1, "source": "test.pdf", "chunk_id": "test_1_2"}
        ), 0.93),
        
        # Different content from same page (should be kept if under limit)
        (Document(
            page_content="Operating expenses increased by 8% to $800 million in 2024.",
            metadata={"page": 1, "source": "test.pdf", "chunk_id": "test_1_3"}
        ), 0.90),
        
        # Content from different page (should be kept)
        (Document(
            page_content="Cash flow from operations was $400 million in 2024.",
            metadata={"page": 2, "source": "test.pdf", "chunk_id": "test_2_1"}
        ), 0.88),
        
        # Another similar content from page 1 (should be filtered due to page limit)
        (Document(
            page_content="The net profit margin improved to 12% in 2024.",
            metadata={"page": 1, "source": "test.pdf", "chunk_id": "test_1_4"}
        ), 0.85),
    ]
    
    return documents

def test_deduplication():
    """Test the deduplication functionality"""
    logger.info("Testing source deduplication functionality")

    # Reload settings to get latest values
    from config import Settings
    global settings
    settings = Settings()

    # Create a mock RAG pipeline instance
    class MockVectorStore:
        def similarity_search(self, query, k=5):
            return create_test_documents()

    # Create RAG pipeline with mock vector store
    rag_pipeline = RAGPipeline(MockVectorStore())

    # Test with deduplication enabled
    logger.info("\n=== Testing with deduplication ENABLED ===")
    logger.info(f"Current settings: threshold={settings.content_similarity_threshold}, max_per_page={settings.max_sources_per_page}")
    settings.enable_source_deduplication = True
    
    test_docs = create_test_documents()
    sources_with_dedup = rag_pipeline._prepare_sources(test_docs)
    
    logger.info(f"Original documents: {len(test_docs)}")
    logger.info(f"After deduplication: {len(sources_with_dedup)}")
    
    for i, source in enumerate(sources_with_dedup):
        logger.info(f"Source {i+1}: Page {source['page']}, Score: {source['score']}")
        logger.info(f"  Content: {source['content'][:100]}...")
    
    # Test with deduplication disabled
    logger.info("\n=== Testing with deduplication DISABLED ===")
    settings.enable_source_deduplication = False
    
    sources_without_dedup = rag_pipeline._prepare_sources(test_docs)
    
    logger.info(f"Original documents: {len(test_docs)}")
    logger.info(f"Without deduplication: {len(sources_without_dedup)}")
    
    for i, source in enumerate(sources_without_dedup):
        logger.info(f"Source {i+1}: Page {source['page']}, Score: {source['score']}")
        logger.info(f"  Content: {source['content'][:100]}...")
    
    # Test content similarity calculation
    logger.info("\n=== Testing content similarity calculation ===")
    content1 = "The company's total revenue for 2024 was $1.2 billion"
    content2 = "Total revenue for 2024 reached $1.2 billion"
    content3 = "Operating expenses increased by 8% to $800 million"
    
    similarity1_2 = rag_pipeline._calculate_content_similarity(content1, content2)
    similarity1_3 = rag_pipeline._calculate_content_similarity(content1, content3)
    
    logger.info(f"Similarity between similar contents: {similarity1_2:.3f}")
    logger.info(f"Similarity between different contents: {similarity1_3:.3f}")
    logger.info(f"Similarity threshold: {settings.content_similarity_threshold}")

if __name__ == "__main__":
    test_deduplication()
