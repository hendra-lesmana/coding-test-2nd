from typing import List, Dict, Any, Tuple
from langchain.schema import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from services.vector_store import VectorStoreService
from config import settings
import logging
import time

logger = logging.getLogger(__name__)


class RAGPipeline:
    def __init__(self, vector_store_service: VectorStoreService):
        """Initialize RAG pipeline components"""
        try:
            self.vector_store = vector_store_service

            # Try to initialize Google Gemini LLM first, fallback to local model
            try:
                if settings.google_api_key and settings.google_api_key.strip():
                    self.llm = ChatGoogleGenerativeAI(
                        model=settings.llm_model,
                        google_api_key=settings.google_api_key,
                        temperature=settings.llm_temperature,
                        max_tokens=settings.max_tokens
                    )
                    self.use_chat_model = True
                    logger.info("Using Google Gemini model")
                else:
                    raise ValueError("No Google API key provided")
            except Exception as e:
                logger.warning(f"Google Gemini LLM failed: {str(e)}, using fallback response")
                self.llm = None
                self.use_chat_model = False
                logger.info("Using fallback text generation (no LLM)")

            # Initialize prompt templates
            self._setup_prompt_templates()

            logger.info("RAGPipeline initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing RAGPipeline: {str(e)}")
            raise

    def _setup_prompt_templates(self):
        """Setup prompt templates for different scenarios"""

        # System prompt for financial Q&A
        system_template = """You are an expert financial analyst assistant. Your task is to answer questions about financial statements based on the provided context.

Guidelines:
1. Answer questions accurately based ONLY on the provided context
2. If the context doesn't contain enough information, clearly state that
3. Provide specific numbers, percentages, and financial metrics when available
4. Explain financial concepts clearly for better understanding
5. If asked about trends, compare different periods when data is available
6. Always cite the specific sections or pages from the context when possible

Context from financial documents:
{context}

Previous conversation (if any):
{chat_history}
"""

        human_template = """Question: {question}

Please provide a comprehensive answer based on the financial document context provided above."""

        self.prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template(human_template)
        ])

    def generate_answer(self, question: str, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Generate answer using RAG pipeline"""
        start_time = time.time()

        try:
            logger.info(f"Generating answer for question: '{question[:100]}...'")

            # Step 1: Retrieve relevant documents
            retrieved_docs = self._retrieve_documents(question)

            if not retrieved_docs:
                return {
                    "answer": "I couldn't find relevant information in the financial documents to answer your question. Please try rephrasing your question or ensure the document contains the information you're looking for.",
                    "sources": [],
                    "processing_time": time.time() - start_time
                }

            # Step 2: Generate context from retrieved documents
            context = self._generate_context(retrieved_docs)

            # Step 3: Format chat history
            chat_history_str = self._format_chat_history(chat_history)

            # Step 4: Generate answer using LLM
            answer = self._generate_llm_response(question, context, chat_history_str)

            # Step 5: Prepare sources information
            sources = self._prepare_sources(retrieved_docs)

            processing_time = time.time() - start_time

            logger.info(f"Answer generated successfully in {processing_time:.2f} seconds")

            return {
                "answer": answer,
                "sources": sources,
                "processing_time": processing_time
            }

        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            return {
                "answer": f"I encountered an error while processing your question: {str(e)}",
                "sources": [],
                "processing_time": time.time() - start_time
            }

    def _retrieve_documents(self, query: str) -> List[Tuple[Document, float]]:
        """Retrieve relevant documents for the query"""
        try:
            # Search vector store for similar documents
            results = self.vector_store.similarity_search(query, k=settings.retrieval_k)

            logger.info(f"Retrieved {len(results)} relevant documents")
            return results

        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []

    def _generate_context(self, documents: List[Tuple[Document, float]]) -> str:
        """Generate context from retrieved documents"""
        if not documents:
            return "No relevant context found."

        context_parts = []
        for i, (doc, score) in enumerate(documents, 1):
            metadata = doc.metadata
            source_info = f"Source {i} (Page {metadata.get('page', 'Unknown')}, Similarity: {score:.3f}):"
            content = doc.page_content
            context_parts.append(f"{source_info}\n{content}\n")

        context = "\n".join(context_parts)
        logger.info(f"Generated context from {len(documents)} documents")
        return context

    def _format_chat_history(self, chat_history: List[Dict[str, str]] = None) -> str:
        """Format chat history for context"""
        if not chat_history:
            return "No previous conversation."

        formatted_history = []
        for entry in chat_history[-5:]:  # Keep only last 5 exchanges
            role = entry.get('role', 'unknown')
            content = entry.get('content', '')
            formatted_history.append(f"{role.capitalize()}: {content}")

        return "\n".join(formatted_history)

    def _generate_llm_response(self, question: str, context: str, chat_history: str) -> str:
        """Generate response using LLM or fallback method"""
        try:
            if self.llm and self.use_chat_model:
                # Create the prompt
                messages = self.prompt_template.format_messages(
                    context=context,
                    chat_history=chat_history,
                    question=question
                )

                # Generate response
                response = self.llm(messages)
                return response.content.strip()
            else:
                # Fallback: Generate a simple response based on context
                return self._generate_fallback_response(question, context)

        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}, using fallback")
            return self._generate_fallback_response(question, context)

    def _generate_fallback_response(self, question: str, context: str) -> str:
        """Generate a fallback response when LLM is not available"""
        try:
            # Simple keyword-based response generation
            context_lines = context.split('\n')
            relevant_lines = []

            # Extract lines that might be relevant to the question
            question_words = question.lower().split()
            for line in context_lines:
                if any(word in line.lower() for word in question_words if len(word) > 3):
                    relevant_lines.append(line.strip())

            if relevant_lines:
                response = f"Based on the financial document, here's what I found related to your question:\n\n"
                response += "\n".join(relevant_lines[:5])  # Limit to first 5 relevant lines
                response += f"\n\nNote: This is a simplified response. For more detailed analysis, please ensure your OpenAI API key is properly configured."
            else:
                response = f"I found information in the document, but couldn't extract specific details related to '{question}'. "
                response += "Please try rephrasing your question or ensure your OpenAI API key is properly configured for detailed analysis."

            return response

        except Exception as e:
            logger.error(f"Error in fallback response generation: {str(e)}")
            return "I apologize, but I'm unable to process your question at the moment. Please check your configuration and try again."

    def _prepare_sources(self, documents: List[Tuple[Document, float]]) -> List[Dict[str, Any]]:
        """Prepare sources information for response"""
        sources = []

        for doc, score in documents:
            metadata = doc.metadata
            source = {
                "content": doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content,
                "page": metadata.get('page', 0),
                "score": round(score, 3),
                "metadata": {
                    "source": metadata.get('source', 'Unknown'),
                    "chunk_id": metadata.get('chunk_id', 'Unknown')
                }
            }
            sources.append(source)

        return sources