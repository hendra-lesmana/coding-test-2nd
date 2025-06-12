#!/usr/bin/env python3
"""
Test script to directly test the new financial data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.rag_pipeline import RAGPipeline
from services.vector_store import VectorStoreService
from config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_specific_financial_questions():
    """Test specific financial questions with the current vector store"""
    
    # Initialize services
    logger.info("🚀 Initializing RAG system...")
    vector_store = VectorStoreService()
    rag_pipeline = RAGPipeline(vector_store)
    
    # Test questions that should work with the new data
    test_questions = [
        "What is the total revenue for 2024?",
        "What is the operating profit growth rate?", 
        "What are the operating expenses?",
        "What is the cash and cash equivalents?",
        "What is the debt-to-equity ratio?",
        "What is the net income?",
        "What is the return on equity?"
    ]
    
    logger.info(f"🧪 Testing {len(test_questions)} financial questions...\n")
    
    for i, question in enumerate(test_questions, 1):
        logger.info(f"{'='*60}")
        logger.info(f"Question {i}: {question}")
        logger.info(f"{'='*60}")
        
        try:
            # Generate answer
            result = rag_pipeline.generate_answer(question)
            
            # Display results
            logger.info(f"📝 Answer: {result['answer']}")
            logger.info(f"⏱️ Processing Time: {result['processing_time']:.2f}s")
            logger.info(f"📚 Sources Found: {len(result['sources'])}")
            
            for j, source in enumerate(result['sources'], 1):
                logger.info(f"  Source {j}: Page {source['page']}, Score: {source['score']}")
                logger.info(f"    Content: {source['content'][:150]}...")
            
            logger.info("")
            
        except Exception as e:
            logger.error(f"❌ Error processing question: {str(e)}")
            logger.info("")

def check_vector_store_contents():
    """Check what's actually in the vector store"""
    logger.info("🔍 Checking vector store contents...")
    
    vector_store = VectorStoreService()
    
    # Try a very specific search for the new data
    test_queries = [
        "Total Revenue 1200000000",
        "Operating Income 340000000", 
        "Cash and Cash Equivalents 320000000",
        "Debt-to-Equity Ratio 0.57"
    ]
    
    for query in test_queries:
        logger.info(f"\n🔍 Searching for: '{query}'")
        results = vector_store.similarity_search(query, k=3)
        
        if results:
            for i, (doc, score) in enumerate(results, 1):
                logger.info(f"  Result {i}: Score {score:.3f}, Page {doc.metadata.get('page', 'N/A')}")
                logger.info(f"    Content: {doc.page_content[:200]}...")
        else:
            logger.info("  No results found")

def main():
    """Main test function"""
    logger.info("🎯 Testing New Financial Data\n")
    
    # Check what's in the vector store
    check_vector_store_contents()
    
    logger.info("\n" + "="*80 + "\n")
    
    # Test financial questions
    test_specific_financial_questions()
    
    logger.info("✅ Test completed!")

if __name__ == "__main__":
    main()
