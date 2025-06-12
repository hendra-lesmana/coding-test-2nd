import os
from typing import List, Dict, Any
import PyPDF2
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from config import settings
import logging

logger = logging.getLogger(__name__)


class PDFProcessor:
    def __init__(self):
        """Initialize PDF processor with text splitter"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        logger.info(f"PDFProcessor initialized with chunk_size={settings.chunk_size}, overlap={settings.chunk_overlap}")

    def extract_text_from_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract text from PDF and return page-wise content"""
        pages_content = []

        try:
            # Use pdfplumber for better text extraction
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text and text.strip():
                        pages_content.append({
                            "page_number": page_num,
                            "content": text.strip(),
                            "metadata": {
                                "source": os.path.basename(file_path),
                                "page": page_num,
                                "total_pages": len(pdf.pages)
                            }
                        })

            logger.info(f"Extracted text from {len(pages_content)} pages from {file_path}")
            return pages_content

        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {str(e)}")
            # Fallback to PyPDF2
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page_num, page in enumerate(pdf_reader.pages, 1):
                        text = page.extract_text()
                        if text and text.strip():
                            pages_content.append({
                                "page_number": page_num,
                                "content": text.strip(),
                                "metadata": {
                                    "source": os.path.basename(file_path),
                                    "page": page_num,
                                    "total_pages": len(pdf_reader.pages)
                                }
                            })
                    logger.info(f"Fallback: Extracted text from {len(pages_content)} pages using PyPDF2")
                    return pages_content
            except Exception as fallback_error:
                logger.error(f"Fallback PDF extraction also failed: {str(fallback_error)}")
                raise Exception(f"Failed to extract text from PDF: {str(e)}")

    def split_into_chunks(self, pages_content: List[Dict[str, Any]]) -> List[Document]:
        """Split page content into chunks"""
        documents = []

        for page_data in pages_content:
            page_content = page_data["content"]
            page_metadata = page_data["metadata"]

            # Split the page content into chunks
            chunks = self.text_splitter.split_text(page_content)

            for chunk_idx, chunk in enumerate(chunks):
                if chunk.strip():  # Only add non-empty chunks
                    # Create metadata for this chunk
                    chunk_metadata = page_metadata.copy()
                    chunk_metadata.update({
                        "chunk_index": chunk_idx,
                        "chunk_id": f"{page_metadata['source']}_page_{page_metadata['page']}_chunk_{chunk_idx}"
                    })

                    # Create Document object
                    doc = Document(
                        page_content=chunk.strip(),
                        metadata=chunk_metadata
                    )
                    documents.append(doc)

        logger.info(f"Split content into {len(documents)} chunks")
        return documents

    def process_pdf(self, file_path: str) -> List[Document]:
        """Process PDF file and return list of Document objects"""
        try:
            logger.info(f"Starting PDF processing for: {file_path}")

            # Step 1: Extract text from PDF
            pages_content = self.extract_text_from_pdf(file_path)

            if not pages_content:
                raise Exception("No text content extracted from PDF")

            # Step 2: Split text into chunks
            documents = self.split_into_chunks(pages_content)

            if not documents:
                raise Exception("No document chunks created")

            logger.info(f"Successfully processed PDF: {len(documents)} chunks created")
            return documents

        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
            raise