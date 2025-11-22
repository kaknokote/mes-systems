import React from 'react';
import ChatGPTChat from '../components/ChatGPTChat';
import { ArrowLeft } from 'lucide-react';

const ChatPage = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-6">
        <button
          onClick={() => window.history.back()}
          className="flex items-center text-gray-600 hover:text-gray-800 mb-4"
        >
          <ArrowLeft size={16} className="mr-2" />
          Back
        </button>
        <h1 className="text-3xl font-bold text-gray-900">AI Assistant</h1>
        <p className="text-gray-600 mt-2">
          Chat with our AI assistant for help with your items and more
        </p>
      </div>

      <ChatGPTChat />
    </div>
  );
};

export default ChatPage;
