#!/usr/bin/env python3
"""
Test script to verify the system works without OpenAI API
"""

import os
import sys
import tempfile

# Add backend to path
sys.path.append('backend')

def test_pdf_processing():
    """Test PDF processing without OpenAI"""
    try:
        from services.pdf_processor import PDFProcessor
        
        print("✅ PDF processor import successful")
        
        # Test with sample PDF if available
        sample_pdf = "data/sample.pdf"
        if os.path.exists(sample_pdf):
            processor = PDFProcessor()
            print("✅ PDF processor initialized")
            
            # Test processing (just first few pages to avoid long processing)
            print(f"📄 Testing with {sample_pdf}")
            documents = processor.process_pdf(sample_pdf)
            print(f"✅ PDF processed successfully: {len(documents)} chunks created")
            return True
        else:
            print("⚠️  No sample PDF found, skipping processing test")
            return True
            
    except Exception as e:
        print(f"❌ PDF processing test failed: {e}")
        return False

def test_vector_store():
    """Test vector store with local embeddings"""
    try:
        # Temporarily remove OpenAI key to force local embeddings
        original_key = os.environ.get('OPENAI_API_KEY')
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        
        from services.vector_store import VectorStoreService
        from langchain.schema import Document
        
        print("✅ Vector store import successful")
        
        # Initialize with local embeddings
        vector_store = VectorStoreService()
        print("✅ Vector store initialized with local embeddings")
        
        # Test with sample documents
        test_docs = [
            Document(page_content="This is a test financial document about revenue.", 
                    metadata={"page": 1, "source": "test.pdf"}),
            Document(page_content="The company's expenses increased by 10% this year.", 
                    metadata={"page": 2, "source": "test.pdf"})
        ]
        
        vector_store.add_documents(test_docs)
        print("✅ Documents added to vector store")
        
        # Test search
        results = vector_store.similarity_search("revenue", k=1)
        print(f"✅ Similarity search successful: {len(results)} results")
        
        # Restore original key
        if original_key:
            os.environ['OPENAI_API_KEY'] = original_key
        
        return True
        
    except Exception as e:
        print(f"❌ Vector store test failed: {e}")
        # Restore original key
        if original_key:
            os.environ['OPENAI_API_KEY'] = original_key
        return False

def test_rag_pipeline():
    """Test RAG pipeline with fallback"""
    try:
        # Temporarily remove OpenAI key to force fallback
        original_key = os.environ.get('OPENAI_API_KEY')
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        
        from services.vector_store import VectorStoreService
        from services.rag_pipeline import RAGPipeline
        from langchain.schema import Document
        
        print("✅ RAG pipeline import successful")
        
        # Initialize components
        vector_store = VectorStoreService()
        rag_pipeline = RAGPipeline(vector_store)
        print("✅ RAG pipeline initialized with fallback mode")
        
        # Add test documents
        test_docs = [
            Document(page_content="The total revenue for 2025 is $1.2 billion.", 
                    metadata={"page": 1, "source": "test.pdf"}),
            Document(page_content="Operating expenses were $800 million in 2025.", 
                    metadata={"page": 2, "source": "test.pdf"})
        ]
        
        vector_store.add_documents(test_docs)
        
        # Test question answering
        result = rag_pipeline.generate_answer("What is the total revenue?")
        print(f"✅ Question answering successful")
        print(f"📝 Answer: {result['answer'][:100]}...")
        
        # Restore original key
        if original_key:
            os.environ['OPENAI_API_KEY'] = original_key
        
        return True
        
    except Exception as e:
        print(f"❌ RAG pipeline test failed: {e}")
        # Restore original key
        if original_key:
            os.environ['OPENAI_API_KEY'] = original_key
        return False

def main():
    print("🧪 Testing RAG System Without OpenAI API")
    print("=" * 50)
    
    # Change to backend directory
    if os.path.exists('backend'):
        os.chdir('backend')
    
    print("\n1. Testing PDF Processing...")
    pdf_ok = test_pdf_processing()
    
    print("\n2. Testing Vector Store with Local Embeddings...")
    vector_ok = test_vector_store()
    
    print("\n3. Testing RAG Pipeline with Fallback...")
    rag_ok = test_rag_pipeline()
    
    print("\n" + "=" * 50)
    if pdf_ok and vector_ok and rag_ok:
        print("🎉 All tests passed! The system can work without OpenAI API.")
        print("💡 You can use the system with local embeddings and fallback responses.")
        print("📝 To get better responses, add a valid OpenAI API key to backend/.env")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
        print("🔧 You may need to install additional dependencies:")
        print("   pip install sentence-transformers transformers torch")

if __name__ == "__main__":
    main()
