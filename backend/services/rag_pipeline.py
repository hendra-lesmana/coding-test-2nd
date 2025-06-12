from typing import List, Dict, Any, Tuple
from langchain.schema import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from services.vector_store import VectorStoreService
from config import settings
import logging
import time
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class RAGPipeline:
    def __init__(self, vector_store_service: VectorStoreService):
        """Initialize RAG pipeline components"""
        try:
            self.vector_store = vector_store_service

            # Try to initialize Google Gemini LLM first, fallback to local model
            try:
                if settings.google_api_key and settings.google_api_key.strip():
                    logger.info(f"Initializing Google Gemini model: {settings.llm_model}")
                    self.llm = ChatGoogleGenerativeAI(
                        model=settings.llm_model,
                        google_api_key=settings.google_api_key,
                        temperature=settings.llm_temperature,
                        max_tokens=settings.max_tokens
                    )
                    self.use_chat_model = True
                    logger.info("✅ Google Gemini model initialized successfully")

                    # Test the API connection
                    try:
                        test_response = self.llm.invoke("Test connection")
                        logger.info("✅ Google Gemini API connection verified")
                    except Exception as test_e:
                        logger.error(f"❌ Google Gemini API test failed: {str(test_e)}")
                        raise test_e

                else:
                    raise ValueError("No Google API key provided")
            except Exception as e:
                logger.error(f"❌ Google Gemini LLM initialization failed: {str(e)}")
                logger.warning("🔄 Falling back to simple text processing")
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

        # Enhanced system prompt for financial Q&A
        system_template = """You are an expert financial analyst assistant specializing in financial statement analysis. Your task is to provide comprehensive answers about financial data based on the provided context.

FINANCIAL ANALYSIS GUIDELINES:
1. **Revenue Analysis**: When asked about revenue, provide total figures, growth rates, and segment breakdowns if available
2. **Profitability Metrics**: Calculate and explain profit margins, operating profit growth, net income changes
3. **Cost Analysis**: Identify and categorize main cost items (COGS, operating expenses, interest, taxes)
4. **Cash Flow Assessment**: Analyze operating, investing, and financing cash flows; comment on liquidity
5. **Financial Ratios**: Calculate debt ratios, current ratios, ROE, ROA when data is available
6. **Trend Analysis**: Compare year-over-year changes and identify patterns
7. **Context Citation**: Always reference specific pages and sections from the source documents

RESPONSE FORMAT:
- Start with a direct answer to the question
- Provide specific numbers with currency and time periods
- Include relevant calculations and percentages
- Cite page references for all data points
- If data is incomplete, clearly state what's missing

IMPORTANT: Base your analysis ONLY on the provided context. If information is not available in the context, explicitly state this limitation.

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
        """Generate an enhanced fallback response when LLM is not available"""
        try:
            # Enhanced keyword-based response generation for financial questions
            context_lines = context.split('\n')
            relevant_lines = []

            # Financial keywords mapping
            financial_keywords = {
                'revenue': ['revenue', 'sales', 'income', 'turnover'],
                'profit': ['profit', 'earnings', 'net income', 'operating income'],
                'cost': ['cost', 'expense', 'expenditure', 'cogs'],
                'cash': ['cash', 'cash flow', 'liquidity'],
                'debt': ['debt', 'liability', 'borrowing', 'loan'],
                'ratio': ['ratio', 'margin', 'percentage', '%']
            }

            # Extract lines that might be relevant to the question
            question_lower = question.lower()
            question_words = question_lower.split()

            # Check for financial keywords
            financial_context = []
            for category, keywords in financial_keywords.items():
                if any(keyword in question_lower for keyword in keywords):
                    for line in context_lines:
                        if any(keyword in line.lower() for keyword in keywords):
                            financial_context.append(line.strip())

            # Also get general relevant lines
            for line in context_lines:
                if any(word in line.lower() for word in question_words if len(word) > 3):
                    relevant_lines.append(line.strip())

            # Combine and deduplicate
            all_relevant = list(dict.fromkeys(financial_context + relevant_lines))  # Remove duplicates while preserving order

            if all_relevant:
                response = f"📊 **Financial Information Found** (Simplified Analysis)\n\n"
                response += f"**Question**: {question}\n\n"
                response += "**Relevant Information from Document**:\n"
                for i, line in enumerate(all_relevant[:7], 1):  # Show up to 7 relevant lines
                    if line.strip() and not line.startswith('Source'):
                        response += f"{i}. {line}\n"

                response += f"\n⚠️ **Note**: This is a basic text extraction. For comprehensive financial analysis including calculations, growth rates, and detailed insights, please ensure your Google Gemini API key is properly configured."
                response += f"\n\n💡 **Tip**: Try questions like 'What is the total revenue?' or 'How is the cash flow situation?' for better results with AI analysis."
            else:
                response = f"📋 **Information Search Results**\n\n"
                response += f"I searched the financial document for information related to '{question}', but couldn't find specific matching content.\n\n"
                response += "**Suggestions**:\n"
                response += "• Try rephrasing your question with different financial terms\n"
                response += "• Check if the document contains the specific information you're looking for\n"
                response += "• Ensure your Google Gemini API key is properly configured for AI-powered analysis\n\n"
                response += "**Common financial questions that work well**:\n"
                response += "• 'What is the total revenue?'\n"
                response += "• 'What is the operating profit growth rate?'\n"
                response += "• 'What are the main cost items?'\n"
                response += "• 'How is the cash flow situation?'\n"
                response += "• 'What is the debt ratio?'"

            return response

        except Exception as e:
            logger.error(f"Error in fallback response generation: {str(e)}")
            return "❌ I apologize, but I'm unable to process your question at the moment. Please check your Google Gemini API configuration and try again."

    def _prepare_sources(self, documents: List[Tuple[Document, float]]) -> List[Dict[str, Any]]:
        """Prepare sources information for response with deduplication"""
        if not settings.enable_source_deduplication:
            # Return all sources without deduplication
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

        # Apply deduplication
        return self._deduplicate_sources(documents)

    def _deduplicate_sources(self, documents: List[Tuple[Document, float]]) -> List[Dict[str, Any]]:
        """Deduplicate sources based on content similarity and page limits"""
        sources = []
        page_source_count = {}
        processed_contents = []

        for doc, score in documents:
            metadata = doc.metadata
            page_num = metadata.get('page', 0)
            content = doc.page_content

            # Check page limit
            if page_source_count.get(page_num, 0) >= settings.max_sources_per_page:
                logger.debug(f"Skipping source from page {page_num} - max sources per page reached")
                continue

            # Check content similarity with already processed sources
            is_duplicate = False
            for processed_content in processed_contents:
                similarity = self._calculate_content_similarity(content, processed_content)
                if similarity >= settings.content_similarity_threshold:
                    logger.debug(f"Skipping duplicate source (similarity: {similarity:.3f})")
                    is_duplicate = True
                    break

            if not is_duplicate:
                source = {
                    "content": content[:500] + "..." if len(content) > 500 else content,
                    "page": page_num,
                    "score": round(score, 3),
                    "metadata": {
                        "source": metadata.get('source', 'Unknown'),
                        "chunk_id": metadata.get('chunk_id', 'Unknown')
                    }
                }
                sources.append(source)
                processed_contents.append(content)
                page_source_count[page_num] = page_source_count.get(page_num, 0) + 1

        logger.info(f"Deduplicated sources: {len(documents)} -> {len(sources)}")
        return sources

    def _calculate_content_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity between two content strings"""
        try:
            # Normalize content for comparison
            content1_norm = ' '.join(content1.lower().split())
            content2_norm = ' '.join(content2.lower().split())

            # Use SequenceMatcher to calculate similarity
            similarity = SequenceMatcher(None, content1_norm, content2_norm).ratio()
            return similarity
        except Exception as e:
            logger.warning(f"Error calculating content similarity: {str(e)}")
            return 0.0