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
    <div className="h-screen bg-gray-900 text-white overflow-hidden">
      <Head>
        <title>RAG-based Financial Q&A System</title>
        <meta name="description" content="AI-powered Q&A system for financial documents" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto px-3 py-2 max-w-7xl h-full flex flex-col">
        {/* Compact Header */}
        <div className="text-center mb-3">
          <h1 className="text-2xl font-bold text-white mb-1">
            Financial Q&A System
          </h1>
          <p className="text-sm text-gray-300">
            Upload PDF • Ask Questions • Get AI-powered Insights
          </p>
        </div>

        {/* Compact Notification */}
        {notification && (
          <div className={`mb-2 p-2 rounded text-sm ${
            notification.type === 'success'
              ? 'bg-green-800 text-green-100'
              : 'bg-red-800 text-red-100'
          }`}>
            <div className="flex items-center justify-between">
              <span>{notification.message}</span>
              <button
                onClick={() => setNotification(null)}
                className="ml-2 text-white hover:text-gray-300"
              >
                ×
              </button>
            </div>
          </div>
        )}

        {/* Compact Document Status */}
        {isDocumentUploaded && uploadedDocument && (
          <div className="mb-2 bg-blue-800 rounded p-2 text-sm">
            <div className="flex items-center text-blue-100">
              <svg className="h-4 w-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
              </svg>
              <span>
                {uploadedDocument.filename} • {uploadedDocument.chunks_count} chunks • Ready
              </span>
            </div>
          </div>
        )}

        {/* Compact Main Content */}
        <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-3 min-h-0">
          {/* Left Column - File Upload */}
          <div className="flex flex-col">
            <FileUpload
              onUploadComplete={handleUploadComplete}
              onUploadError={handleUploadError}
            />

            {/* Compact Instructions */}
            <div className="bg-gray-800 rounded p-3 text-sm flex-1">
              <h3 className="font-semibold mb-2 text-white">Quick Guide</h3>
              <div className="text-gray-300 space-y-1 text-xs">
                <p>1. Upload PDF → 2. Wait for processing → 3. Ask questions</p>
                <div className="mt-2">
                  <span className="text-gray-400">Try: </span>
                  <span>"What is the total revenue?" or "How is cash flow?"</span>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Chat Interface */}
          <div className="flex flex-col min-h-0">
            <ChatInterface
              isDocumentUploaded={isDocumentUploaded}
              onError={handleChatError}
            />
          </div>
        </div>

      </main>
    </div>
  );
}