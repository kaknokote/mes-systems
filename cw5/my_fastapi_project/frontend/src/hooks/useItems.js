import { useState, useEffect } from 'react';
import { itemsAPI } from '../services/api';

export const useItems = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Получить все items
  const fetchItems = async (skip = 0, limit = 100, title = '') => {
    setLoading(true);
    setError(null);
    try {
      const response = await itemsAPI.getAll(skip, limit, title);
      setItems(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch items');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Создать item
  const createItem = async (itemData) => {
    setLoading(true);
    setError(null);
    try {
      const response = await itemsAPI.create(itemData);
      setItems(prev => [...prev, response.data]);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create item');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Обновить item
  const updateItem = async (id, itemData) => {
    setLoading(true);
    setError(null);
    try {
      const response = await itemsAPI.update(id, itemData);
      setItems(prev => prev.map(item => 
        item.id === id ? response.data : item
      ));
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update item');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Удалить item
  const deleteItem = async (id) => {
    setLoading(true);
    setError(null);
    try {
      await itemsAPI.delete(id);
      setItems(prev => prev.filter(item => item.id !== id));
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete item');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Анализировать с ChatGPT
  const analyzeItem = async (id) => {
    setLoading(true);
    setError(null);
    try {
      const response = await itemsAPI.analyze(id);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze item');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  return {
    items,
    loading,
    error,
    fetchItems,
    createItem,
    updateItem,
    deleteItem,
    analyzeItem,
  };
};
