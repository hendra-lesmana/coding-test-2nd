import React, { useState, useRef } from 'react';
import axios from 'axios';

interface FileUploadProps {
  onUploadComplete?: (result: any) => void;
  onUploadError?: (error: string) => void;
}

export default function FileUpload({ onUploadComplete, onUploadError }: FileUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = (selectedFile: File): string | null => {
    // Validate file type
    if (selectedFile.type !== 'application/pdf') {
      return 'Please select a PDF file only.';
    }

    // Validate file size (max 50MB)
    const maxSize = 50 * 1024 * 1024; // 50MB
    if (selectedFile.size > maxSize) {
      return 'File size must be less than 50MB.';
    }

    return null;
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      const error = validateFile(selectedFile);
      if (error) {
        onUploadError?.(error);
        return;
      }
      setFile(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    setUploadProgress(0);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('http://localhost:8000/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            setUploadProgress(progress);
          }
        },
      });

      onUploadComplete?.(response.data);
      setFile(null);
      setUploadProgress(0);

      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }

    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Upload failed. Please try again.';
      onUploadError?.(errorMessage);
    } finally {
      setIsUploading(false);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      const error = validateFile(droppedFile);
      if (error) {
        onUploadError?.(error);
        return;
      }
      setFile(droppedFile);
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="file-upload bg-gray-800 rounded p-3 mb-2">
      <h3 className="text-sm font-semibold mb-2 text-white">Upload PDF</h3>

      {/* Compact Drag & Drop area */}
      <div
        className={`upload-area border-2 border-dashed rounded p-4 text-center transition-colors ${
          isDragOver
            ? 'border-blue-400 bg-blue-900'
            : 'border-gray-600 hover:border-gray-500'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="flex flex-col items-center">
          <svg className="w-6 h-6 text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>

          {file ? (
            <div className="text-center">
              <p className="text-xs font-medium text-white">{file.name}</p>
              <p className="text-xs text-gray-400">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          ) : (
            <div className="text-center">
              <p className="text-xs text-gray-300 mb-1">
                Drop PDF here or{' '}
                <button
                  type="button"
                  className="text-blue-400 hover:text-blue-300 font-medium"
                  onClick={handleBrowseClick}
                >
                  browse
                </button>
              </p>
              <p className="text-xs text-gray-500">Max 50MB</p>
            </div>
          )}
        </div>
      </div>

      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf"
        onChange={handleFileSelect}
        className="hidden"
      />

      {/* Compact Upload button */}
      {file && (
        <div className="mt-2">
          <button
            onClick={handleUpload}
            disabled={isUploading}
            className={`w-full py-1 px-3 rounded text-sm font-medium transition-colors ${
              isUploading
                ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {isUploading ? `Uploading... ${uploadProgress}%` : 'Upload & Process'}
          </button>
        </div>
      )}

      {/* Compact Progress bar */}
      {isUploading && (
        <div className="mt-2">
          <div className="bg-gray-700 rounded-full h-1">
            <div
              className="bg-blue-500 h-1 rounded-full transition-all duration-300"
              style={{ width: `${uploadProgress}%` }}
            ></div>
          </div>
          <p className="text-xs text-gray-400 mt-1 text-center">
            Processing document...
          </p>
        </div>
      )}
    </div>
  );
}