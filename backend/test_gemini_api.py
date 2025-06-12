#!/usr/bin/env python3
"""
Test script to validate Google Gemini API configuration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_gemini_api():
    """Test Google Gemini API connection and functionality"""
    logger.info("🔍 Testing Google Gemini API Configuration")
    
    # Check API key
    if not settings.google_api_key:
        logger.error("❌ No Google API key found in configuration")
        logger.info("💡 Please set GOOGLE_API_KEY in your .env file")
        return False
    
    logger.info(f"✅ API Key found: {settings.google_api_key[:10]}...")
    logger.info(f"📋 Model: {settings.llm_model}")
    logger.info(f"🌡️ Temperature: {settings.llm_temperature}")
    logger.info(f"📝 Max Tokens: {settings.max_tokens}")
    
    # Test API connection
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        logger.info("🔄 Initializing Gemini model...")
        llm = ChatGoogleGenerativeAI(
            model=settings.llm_model,
            google_api_key=settings.google_api_key,
            temperature=settings.llm_temperature,
            max_tokens=settings.max_tokens
        )
        
        logger.info("✅ Model initialized successfully")
        
        # Test simple query
        logger.info("🧪 Testing simple query...")
        test_response = llm.invoke("Hello, can you respond with 'API test successful'?")
        logger.info(f"📤 Response: {test_response.content}")
        
        # Test financial analysis query
        logger.info("🧪 Testing financial analysis query...")
        financial_test = """
        Based on this financial data:
        Revenue: $1.2 billion (15% growth)
        Operating expenses: $800 million
        Net income: $300 million
        
        What is the profit margin?
        """
        
        financial_response = llm.invoke(financial_test)
        logger.info(f"📊 Financial Analysis Response: {financial_response.content}")
        
        logger.info("🎉 Google Gemini API is working correctly!")
        return True
        
    except Exception as e:
        logger.error(f"❌ API test failed: {str(e)}")
        
        # Provide specific error guidance
        error_str = str(e).lower()
        if "api key" in error_str or "authentication" in error_str:
            logger.info("💡 API Key Issue: Please check if your Google API key is valid and has Gemini API access enabled")
        elif "quota" in error_str or "limit" in error_str:
            logger.info("💡 Quota Issue: You may have exceeded your API quota or rate limits")
        elif "model" in error_str:
            logger.info(f"💡 Model Issue: The model '{settings.llm_model}' may not be available. Try 'gemini-1.5-flash' or 'gemini-1.5-pro'")
        else:
            logger.info("💡 General Issue: Check your internet connection and API configuration")
        
        return False

def test_embeddings():
    """Test Google Gemini embeddings"""
    logger.info("\n🔍 Testing Google Gemini Embeddings")
    
    try:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        
        embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.google_api_key
        )
        
        # Test embedding generation
        test_text = "This is a test for financial document embedding"
        embedding = embeddings.embed_query(test_text)
        
        logger.info(f"✅ Embeddings working - Vector dimension: {len(embedding)}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Embeddings test failed: {str(e)}")
        return False

def main():
    """Main test function"""
    logger.info("🚀 Starting Google Gemini API Tests\n")
    
    # Test LLM
    llm_success = test_gemini_api()
    
    # Test Embeddings
    embeddings_success = test_embeddings()
    
    # Summary
    logger.info("\n📋 Test Summary:")
    logger.info(f"LLM API: {'✅ Working' if llm_success else '❌ Failed'}")
    logger.info(f"Embeddings API: {'✅ Working' if embeddings_success else '❌ Failed'}")
    
    if llm_success and embeddings_success:
        logger.info("\n🎉 All tests passed! Your Gemini API is properly configured.")
        logger.info("You should now be able to ask financial questions and get AI-powered responses.")
    else:
        logger.info("\n⚠️ Some tests failed. Please check your API configuration.")
        logger.info("The system will fall back to basic text extraction until the API is working.")

if __name__ == "__main__":
    main()
