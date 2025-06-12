#!/usr/bin/env python3
"""
Test script to simulate the full RAG workflow with financial questions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.rag_pipeline import RAGPipeline
from services.vector_store import VectorStoreService
from langchain.schema import Document
from config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_financial_documents():
    """Create sample financial documents for testing"""
    documents = [
        Document(
            page_content="""
            FINANCIAL HIGHLIGHTS
            Total Revenue: $1.2 billion (15% increase from previous year)
            Operating Revenue: $1.1 billion
            Net Revenue: $1.0 billion
            Revenue Growth Rate: 15% year-over-year
            """,
            metadata={"page": 1, "source": "financial_statement.pdf", "chunk_id": "fs_1_1"}
        ),
        Document(
            page_content="""
            PROFITABILITY ANALYSIS
            Operating Profit: $400 million (20% increase)
            Net Income: $300 million
            Operating Profit Margin: 33.3%
            Net Profit Margin: 25%
            Year-over-year Operating Profit Growth Rate: 20%
            """,
            metadata={"page": 2, "source": "financial_statement.pdf", "chunk_id": "fs_2_1"}
        ),
        Document(
            page_content="""
            COST STRUCTURE
            Cost of Goods Sold (COGS): $600 million
            Operating Expenses: $200 million
            Administrative Expenses: $50 million
            Marketing Expenses: $30 million
            Research and Development: $70 million
            Total Operating Costs: $950 million
            """,
            metadata={"page": 3, "source": "financial_statement.pdf", "chunk_id": "fs_3_1"}
        ),
        Document(
            page_content="""
            CASH FLOW STATEMENT
            Operating Cash Flow: $450 million (positive)
            Investing Cash Flow: -$100 million
            Financing Cash Flow: -$50 million
            Net Cash Flow: $300 million
            Cash and Cash Equivalents: $800 million
            Free Cash Flow: $350 million
            """,
            metadata={"page": 4, "source": "financial_statement.pdf", "chunk_id": "fs_4_1"}
        ),
        Document(
            page_content="""
            BALANCE SHEET HIGHLIGHTS
            Total Assets: $2.5 billion
            Total Liabilities: $1.2 billion
            Total Debt: $800 million
            Shareholders' Equity: $1.3 billion
            Debt-to-Equity Ratio: 0.62
            Current Ratio: 2.1
            Quick Ratio: 1.8
            """,
            metadata={"page": 5, "source": "financial_statement.pdf", "chunk_id": "fs_5_1"}
        )
    ]
    return documents

def test_financial_questions():
    """Test the system with various financial questions"""
    
    # Initialize services
    logger.info("🚀 Initializing RAG system...")
    vector_store = VectorStoreService()
    rag_pipeline = RAGPipeline(vector_store)
    
    # Add sample documents
    logger.info("📄 Adding sample financial documents...")
    sample_docs = create_sample_financial_documents()
    vector_store.add_documents(sample_docs)
    
    # Test questions
    test_questions = [
        "What is the total revenue?",
        "What is the year-over-year operating profit growth rate?",
        "What are the main cost items?",
        "How is the cash flow situation?",
        "What is the debt ratio?"
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
                logger.info(f"    Content: {source['content'][:100]}...")
            
            logger.info("")
            
        except Exception as e:
            logger.error(f"❌ Error processing question: {str(e)}")
            logger.info("")

def test_empty_vector_store():
    """Test what happens with no documents"""
    logger.info("🧪 Testing with empty vector store...")
    
    vector_store = VectorStoreService()
    rag_pipeline = RAGPipeline(vector_store)
    
    result = rag_pipeline.generate_answer("What is the total revenue?")
    logger.info(f"📝 Empty store response: {result['answer']}")
    logger.info(f"📚 Sources: {len(result['sources'])}")

def main():
    """Main test function"""
    logger.info("🎯 Starting Full RAG Workflow Test\n")
    
    # Test with empty vector store first
    test_empty_vector_store()
    logger.info("\n" + "="*80 + "\n")
    
    # Test with sample documents
    test_financial_questions()
    
    logger.info("✅ Full workflow test completed!")

if __name__ == "__main__":
    main()
