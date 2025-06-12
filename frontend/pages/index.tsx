import React, { useState } from 'react';
import Head from 'next/head';
import FileUpload from '../components/FileUpload';
import ChatInterface from '../components/ChatInterface';

export default function Home() {
  const [isDocumentUploaded, setIsDocumentUploaded] = useState(false);
  const [uploadedDocument, setUploadedDocument] = useState<any>(null);
  const [notification, setNotification] = useState<{
    type: 'success' | 'error';
    message: string;
  } | null>(null);

  const handleUploadComplete = (result: any) => {
    setIsDocumentUploaded(true);
    setUploadedDocument(result);
    setNotification({
      type: 'success',
      message: `Successfully processed ${result.filename} with ${result.chunks_count} chunks in ${result.processing_time.toFixed(2)}s`
    });

    // Clear notification after 5 seconds
    setTimeout(() => setNotification(null), 5000);
  };

  const handleUploadError = (error: string) => {
    setNotification({
      type: 'error',
      message: error
    });

    // Clear notification after 5 seconds
    setTimeout(() => setNotification(null), 5000);
  };

  const handleChatError = (error: string) => {
    setNotification({
      type: 'error',
      message: error
    });

    // Clear notification after 5 seconds
    setTimeout(() => setNotification(null), 5000);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>RAG-based Financial Q&A System</title>
        <meta name="description" content="AI-powered Q&A system for financial documents" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            RAG-based Financial Q&A System
          </h1>
          <p className="text-xl text-gray-600 mb-2">
            AI-powered analysis of financial statements
          </p>
          <p className="text-gray-500">
            Upload a financial statement PDF and ask questions to get intelligent insights
          </p>
        </div>

        {/* Notification */}
        {notification && (
          <div className={`mb-6 p-4 rounded-md ${
            notification.type === 'success'
              ? 'bg-green-50 border border-green-200 text-green-800'
              : 'bg-red-50 border border-red-200 text-red-800'
          }`}>
            <div className="flex">
              <div className="flex-shrink-0">
                {notification.type === 'success' ? (
                  <svg className="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                ) : (
                  <svg className="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                )}
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium">{notification.message}</p>
              </div>
              <div className="ml-auto pl-3">
                <button
                  onClick={() => setNotification(null)}
                  className="inline-flex text-gray-400 hover:text-gray-600"
                >
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Document Status */}
        {isDocumentUploaded && uploadedDocument && (
          <div className="mb-6 bg-blue-50 border border-blue-200 rounded-md p-4">
            <div className="flex items-center">
              <svg className="h-5 w-5 text-blue-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
              </svg>
              <div>
                <p className="text-sm font-medium text-blue-800">
                  Document Ready: {uploadedDocument.filename}
                </p>
                <p className="text-xs text-blue-600">
                  {uploadedDocument.chunks_count} chunks processed • Ready for questions
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - File Upload */}
          <div>
            <FileUpload
              onUploadComplete={handleUploadComplete}
              onUploadError={handleUploadError}
            />

            {/* Instructions */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold mb-4 text-gray-800">How to Use</h3>
              <ol className="list-decimal list-inside space-y-2 text-sm text-gray-600">
                <li>Upload a financial statement PDF using the upload area above</li>
                <li>Wait for the document to be processed and indexed</li>
                <li>Start asking questions about the financial data in the chat</li>
                <li>Get AI-powered answers with source references</li>
              </ol>

              <div className="mt-4 p-3 bg-gray-50 rounded-md">
                <h4 className="font-medium text-gray-800 mb-2">Sample Questions:</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• "What is the total revenue for 2025?"</li>
                  <li>• "What are the main cost items?"</li>
                  <li>• "How is the cash flow situation?"</li>
                  <li>• "What is the debt ratio?"</li>
                  <li>• "What is the year-over-year growth rate?"</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Right Column - Chat Interface */}
          <div>
            <ChatInterface
              isDocumentUploaded={isDocumentUploaded}
              onError={handleChatError}
            />
          </div>
        </div>

        {/* Footer */}
        <div className="mt-12 text-center text-gray-500 text-sm">
          <p>Powered by RAG (Retrieval Augmented Generation) technology</p>
          <p>Built with Next.js, FastAPI, and OpenAI</p>
        </div>
      </main>
    </div>
  );
}