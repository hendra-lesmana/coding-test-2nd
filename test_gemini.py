#!/usr/bin/env python3
"""
Test script to verify Google Gemini integration
"""

import os
import sys

# Add backend to path
sys.path.append('backend')

def test_gemini_api():
    """Test Google Gemini API connection"""
    try:
        import google.generativeai as genai
        from config import settings
        
        if not settings.google_api_key:
            print("❌ No Google API key found in configuration")
            print("💡 Please add GOOGLE_API_KEY to backend/.env")
            return False
        
        # Configure Gemini
        genai.configure(api_key=settings.google_api_key)
        
        # Test basic API call
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hello, this is a test. Please respond with 'Gemini API is working!'")
        
        if "working" in response.text.lower():
            print("✅ Google Gemini API is working correctly")
            print(f"📝 Response: {response.text}")
            return True
        else:
            print("⚠️  Gemini API responded but with unexpected content")
            print(f"📝 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False

def test_gemini_embeddings():
    """Test Google Gemini embeddings"""
    try:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        from config import settings
        
        if not settings.google_api_key:
            print("❌ No Google API key found for embeddings test")
            return False
        
        # Initialize embeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=settings.google_api_key
        )
        
        # Test embedding generation
        test_text = "This is a test document about financial statements."
        embedding = embeddings.embed_query(test_text)
        
        if embedding and len(embedding) > 0:
            print(f"✅ Gemini embeddings working: {len(embedding)} dimensions")
            return True
        else:
            print("❌ Gemini embeddings failed to generate")
            return False
            
    except Exception as e:
        print(f"❌ Gemini embeddings test failed: {e}")
        return False

def test_gemini_chat():
    """Test Gemini chat model"""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from config import settings
        
        if not settings.google_api_key:
            print("❌ No Google API key found for chat test")
            return False
        
        # Initialize chat model
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=settings.google_api_key,
            temperature=0.1
        )
        
        # Test chat
        response = llm.invoke("What is 2+2? Please answer with just the number.")
        
        if "4" in str(response.content):
            print("✅ Gemini chat model working correctly")
            print(f"📝 Response: {response.content}")
            return True
        else:
            print("⚠️  Gemini chat responded but with unexpected content")
            print(f"📝 Response: {response.content}")
            return False
            
    except Exception as e:
        print(f"❌ Gemini chat test failed: {e}")
        return False

def test_full_rag_pipeline():
    """Test complete RAG pipeline with Gemini"""
    try:
        from services.vector_store import VectorStoreService
        from services.rag_pipeline import RAGPipeline
        from langchain.schema import Document
        
        print("🔧 Testing complete RAG pipeline with Gemini...")
        
        # Initialize services
        vector_store = VectorStoreService()
        rag_pipeline = RAGPipeline(vector_store)
        
        # Add test financial documents
        test_docs = [
            Document(
                page_content="The company's total revenue for 2025 was $1.5 billion, representing a 12% increase from the previous year.",
                metadata={"page": 1, "source": "financial_statement.pdf"}
            ),
            Document(
                page_content="Operating expenses totaled $900 million in 2025, with the largest components being personnel costs ($400M) and technology infrastructure ($300M).",
                metadata={"page": 2, "source": "financial_statement.pdf"}
            ),
            Document(
                page_content="The company's net profit margin improved to 15.2% in 2025, up from 13.8% in 2024, due to operational efficiency improvements.",
                metadata={"page": 3, "source": "financial_statement.pdf"}
            )
        ]
        
        # Add documents to vector store
        vector_store.add_documents(test_docs)
        print("✅ Test documents added to vector store")
        
        # Test question answering
        questions = [
            "What was the total revenue in 2025?",
            "What were the main operating expenses?",
            "How did the profit margin change?"
        ]
        
        for question in questions:
            print(f"\n❓ Question: {question}")
            result = rag_pipeline.generate_answer(question)
            print(f"✅ Answer: {result['answer'][:150]}...")
            print(f"📊 Sources: {len(result['sources'])} documents")
            print(f"⏱️  Processing time: {result['processing_time']:.2f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Full RAG pipeline test failed: {e}")
        return False

def main():
    print("🧪 Testing Google Gemini Integration")
    print("=" * 50)
    
    # Change to backend directory if needed
    if os.path.exists('backend'):
        os.chdir('backend')
    
    print("\n1. Testing Gemini API Connection...")
    api_ok = test_gemini_api()
    
    print("\n2. Testing Gemini Embeddings...")
    embeddings_ok = test_gemini_embeddings()
    
    print("\n3. Testing Gemini Chat Model...")
    chat_ok = test_gemini_chat()
    
    print("\n4. Testing Full RAG Pipeline...")
    rag_ok = test_full_rag_pipeline()
    
    print("\n" + "=" * 50)
    if api_ok and embeddings_ok and chat_ok and rag_ok:
        print("🎉 All Gemini tests passed! The system is ready to use.")
        print("🚀 You can now start the backend and frontend servers.")
        print("📝 Try uploading a PDF and asking questions!")
    else:
        print("⚠️  Some tests failed. Please check:")
        print("1. Your Google API key is correct in backend/.env")
        print("2. All dependencies are installed: pip install google-generativeai langchain-google-genai")
        print("3. Your API key has the necessary permissions")
        
    print("\n📚 For setup help, see GEMINI_SETUP_GUIDE.md")

if __name__ == "__main__":
    main()
