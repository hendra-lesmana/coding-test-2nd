#!/usr/bin/env python3
"""
Script to reset the vector store and add sample financial data
"""

import sys
import os
import shutil
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.vector_store import VectorStoreService
from langchain.schema import Document
from config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear_vector_store():
    """Clear the existing vector store"""
    try:
        if os.path.exists(settings.vector_db_path):
            shutil.rmtree(settings.vector_db_path)
            logger.info(f"✅ Cleared vector store at {settings.vector_db_path}")
        else:
            logger.info("ℹ️ Vector store directory doesn't exist")
    except Exception as e:
        logger.error(f"❌ Error clearing vector store: {str(e)}")

def create_comprehensive_financial_documents():
    """Create comprehensive sample financial documents"""
    documents = [
        Document(
            page_content="""
            INCOME STATEMENT - YEAR ENDED DECEMBER 31, 2024
            
            REVENUE:
            Total Revenue: $1,200,000,000 (15% increase from 2023: $1,043,478,261)
            Product Sales: $900,000,000
            Service Revenue: $300,000,000
            
            COST OF REVENUE:
            Cost of Goods Sold (COGS): $600,000,000
            Gross Profit: $600,000,000
            Gross Profit Margin: 50%
            """,
            metadata={"page": 1, "source": "financial_statement_2024.pdf", "chunk_id": "income_1"}
        ),
        Document(
            page_content="""
            OPERATING EXPENSES:
            Research and Development: $120,000,000
            Sales and Marketing: $80,000,000
            General and Administrative: $60,000,000
            Total Operating Expenses: $260,000,000
            
            OPERATING PROFIT:
            Operating Income: $340,000,000 (20% increase from 2023: $283,333,333)
            Operating Profit Margin: 28.3%
            Year-over-year Operating Profit Growth Rate: 20%
            """,
            metadata={"page": 2, "source": "financial_statement_2024.pdf", "chunk_id": "income_2"}
        ),
        Document(
            page_content="""
            NET INCOME:
            Interest Income: $5,000,000
            Interest Expense: $15,000,000
            Other Income: $2,000,000
            Income Before Tax: $332,000,000
            Income Tax Expense: $82,000,000
            Net Income: $250,000,000
            Net Profit Margin: 20.8%
            Earnings Per Share: $2.50
            """,
            metadata={"page": 3, "source": "financial_statement_2024.pdf", "chunk_id": "income_3"}
        ),
        Document(
            page_content="""
            CASH FLOW STATEMENT - YEAR ENDED DECEMBER 31, 2024
            
            OPERATING ACTIVITIES:
            Net Income: $250,000,000
            Depreciation and Amortization: $80,000,000
            Changes in Working Capital: $20,000,000
            Net Cash from Operating Activities: $350,000,000
            
            INVESTING ACTIVITIES:
            Capital Expenditures: ($120,000,000)
            Acquisitions: ($50,000,000)
            Net Cash from Investing Activities: ($170,000,000)
            """,
            metadata={"page": 4, "source": "financial_statement_2024.pdf", "chunk_id": "cashflow_1"}
        ),
        Document(
            page_content="""
            FINANCING ACTIVITIES:
            Debt Issuance: $100,000,000
            Debt Repayment: ($80,000,000)
            Dividend Payments: ($50,000,000)
            Share Repurchases: ($30,000,000)
            Net Cash from Financing Activities: ($60,000,000)
            
            NET CHANGE IN CASH: $120,000,000
            Cash at Beginning of Year: $200,000,000
            Cash at End of Year: $320,000,000
            Free Cash Flow: $230,000,000
            """,
            metadata={"page": 5, "source": "financial_statement_2024.pdf", "chunk_id": "cashflow_2"}
        ),
        Document(
            page_content="""
            BALANCE SHEET - AS OF DECEMBER 31, 2024
            
            ASSETS:
            Current Assets:
            Cash and Cash Equivalents: $320,000,000
            Accounts Receivable: $180,000,000
            Inventory: $150,000,000
            Total Current Assets: $650,000,000
            
            Non-Current Assets:
            Property, Plant & Equipment: $800,000,000
            Intangible Assets: $200,000,000
            Total Assets: $1,650,000,000
            """,
            metadata={"page": 6, "source": "financial_statement_2024.pdf", "chunk_id": "balance_1"}
        ),
        Document(
            page_content="""
            LIABILITIES AND EQUITY:
            Current Liabilities:
            Accounts Payable: $120,000,000
            Short-term Debt: $80,000,000
            Total Current Liabilities: $200,000,000
            
            Non-Current Liabilities:
            Long-term Debt: $400,000,000
            Total Liabilities: $600,000,000
            
            Shareholders' Equity: $1,050,000,000
            Total Liabilities and Equity: $1,650,000,000
            
            FINANCIAL RATIOS:
            Debt-to-Equity Ratio: 0.57 ($600M / $1,050M)
            Current Ratio: 3.25 ($650M / $200M)
            Quick Ratio: 2.5
            Return on Equity (ROE): 23.8%
            Return on Assets (ROA): 15.2%
            """,
            metadata={"page": 7, "source": "financial_statement_2024.pdf", "chunk_id": "balance_2"}
        )
    ]
    return documents

def main():
    """Main function to reset and populate vector store"""
    logger.info("🔄 Resetting Vector Store with Sample Financial Data")
    
    # Clear existing vector store
    clear_vector_store()
    
    # Initialize new vector store
    logger.info("🚀 Initializing new vector store...")
    vector_store = VectorStoreService()
    
    # Add comprehensive financial documents
    logger.info("📄 Adding comprehensive financial documents...")
    financial_docs = create_comprehensive_financial_documents()
    vector_store.add_documents(financial_docs)
    
    logger.info(f"✅ Successfully added {len(financial_docs)} financial document chunks")
    logger.info("🎉 Vector store is now ready for financial Q&A!")
    
    # Show what questions can now be answered
    logger.info("\n📋 You can now ask questions like:")
    logger.info("• 'What is the total revenue?'")
    logger.info("• 'What is the year-over-year operating profit growth rate?'")
    logger.info("• 'What are the main cost items?'")
    logger.info("• 'How is the cash flow situation?'")
    logger.info("• 'What is the debt ratio?'")
    logger.info("• 'What is the net profit margin?'")
    logger.info("• 'What is the return on equity?'")

if __name__ == "__main__":
    main()
