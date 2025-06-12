import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

interface Source {
  content: string;
  page: number;
  score: number;
  metadata: {
    source: string;
    chunk_id: string;
  };
}

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  timestamp: Date;
}

interface ChatInterfaceProps {
  isDocumentUploaded: boolean;
  onError?: (error: string) => void;
}

export default function ChatInterface({ isDocumentUploaded, onError }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const generateMessageId = () => {
    return Date.now().toString() + Math.random().toString(36).substr(2, 9);
  };

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: generateMessageId(),
      type: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Prepare chat history for context
      const chatHistory = messages.map(msg => ({
        role: msg.type === 'user' ? 'user' : 'assistant',
        content: msg.content
      }));

      const response = await axios.post('http://localhost:8000/api/chat', {
        question: userMessage.content,
        chat_history: chatHistory
      });

      const assistantMessage: Message = {
        id: generateMessageId(),
        type: 'assistant',
        content: response.data.answer,
        sources: response.data.sources,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);

    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Failed to get response. Please try again.';
      onError?.(errorMessage);

      const errorResponse: Message = {
        id: generateMessageId(),
        type: 'assistant',
        content: 'I apologize, but I encountered an error while processing your question. Please try again.',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  const formatTimestamp = (timestamp: Date) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (!isDocumentUploaded) {
    return (
      <div className="chat-interface bg-gray-800 rounded p-3 flex-1 flex items-center justify-center">
        <div className="text-center">
          <svg className="w-8 h-8 text-gray-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <h3 className="text-sm font-medium text-white mb-1">Ready to Chat</h3>
          <p className="text-xs text-gray-400">Upload a PDF to start asking questions</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-interface bg-gray-800 rounded flex flex-col flex-1 min-h-0">
      {/* Compact Header */}
      <div className="border-b border-gray-700 p-2">
        <h3 className="text-sm font-semibold text-white">Financial Q&A</h3>
        <p className="text-xs text-gray-400">Ask questions about your document</p>
      </div>

      {/* Messages display area */}
      <div className="messages flex-1 overflow-y-auto p-2 space-y-2 min-h-0">
        {messages.length === 0 ? (
          <div className="text-center py-4">
            <p className="text-gray-400 mb-2 text-sm">Ask a question about your document!</p>
            <div className="text-xs text-gray-500">
              <p>Try: "What is the revenue?" or "How is cash flow?"</p>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-3/4 rounded p-2 text-sm ${
                message.type === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-700 text-gray-100'
              }`}>
                <div className="whitespace-pre-wrap">{message.content}</div>

                {/* Compact Sources for assistant messages */}
                {message.type === 'assistant' && message.sources && message.sources.length > 0 && (
                  <div className="mt-2 pt-2 border-t border-gray-600">
                    <div className="flex items-center justify-between mb-1">
                      <p className="text-xs font-medium text-gray-300">Sources:</p>
                      <span className="text-xs text-gray-500">
                        {message.sources.length} unique
                      </span>
                    </div>
                    <div className="space-y-1">
                      {message.sources.map((source, index) => (
                        <div key={index} className="text-xs bg-gray-600 rounded p-1">
                          <div className="flex justify-between items-center">
                            <span className="font-medium">Page {source.page}</span>
                            <span className="text-gray-400">Score: {source.score.toFixed(2)}</span>
                          </div>
                          <p className="text-gray-300 mt-1">{source.content.substring(0, 100)}...</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="text-xs opacity-75 mt-1">
                  {formatTimestamp(message.timestamp)}
                </div>
              </div>
            </div>
          ))
        )}

        {/* Compact Loading indicator */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-700 rounded p-2 text-sm">
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-blue-400"></div>
                <span className="text-gray-300">Thinking...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Compact Input area */}
      <div className="border-t border-gray-700 p-2">
        <div className="flex space-x-2">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={handleInputChange}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage();
              }
            }}
            placeholder="Ask about your document..."
            className="flex-1 border border-gray-600 rounded px-2 py-1 text-sm bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!input.trim() || isLoading}
            className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
              !input.trim() || isLoading
                ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}