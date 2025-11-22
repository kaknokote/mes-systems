import { useState } from 'react';
import { chatGPTAPI } from '../services/api';

export const useChatGPT = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = async (messages, temperature = 0.7) => {
    setLoading(true);
    setError(null);
    try {
      const response = await chatGPTAPI.chat(messages, temperature);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to send message');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const analyzeDescription = async (description) => {
    setLoading(true);
    setError(null);
    try {
      const response = await chatGPTAPI.analyzeDescription(description);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze description');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const generateTitles = async (description) => {
    setLoading(true);
    setError(null);
    try {
      const response = await chatGPTAPI.generateTitles(description);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate titles');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    error,
    sendMessage,
    analyzeDescription,
    generateTitles,
  };
};
