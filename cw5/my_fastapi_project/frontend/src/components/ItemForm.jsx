import React, { useState, useEffect } from 'react';
import { useChatGPT } from '../hooks/useChatGPT';
import { Wand2 } from 'lucide-react';

const ItemForm = ({ item, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: ''
  });
  const { generateTitles, analyzeDescription, loading: aiLoading } = useChatGPT();

  useEffect(() => {
    if (item) {
      setFormData({
        title: item.title || '',
        description: item.description || '',
        price: item.price || ''
      });
    }
  }, [item]);

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleGenerateTitle = async () => {
    if (!formData.description) {
      alert('Please enter a description first');
      return;
    }

    if (formData.description.length < 10) {
      alert('Description must be at least 10 characters long');
      return;
    }

    try {
      const result = await generateTitles(formData.description);
      const titles = result.generated_titles.split('\n').filter(t => t.trim());
      const selectedTitle = titles[0]?.replace(/^\d+\.\s*["']?|["']?$/g, '').trim() || titles[0];
      setFormData(prev => ({ ...prev, title: selectedTitle }));
      alert('Title generated successfully!');
    } catch (err) {
      alert(`Error: ${err.response?.data?.detail || 'Failed to generate title'}`);
    }
  };

  const handleImproveDescription = async () => {
    if (!formData.description) {
      alert('Please enter a description first');
      return;
    }

    if (formData.description.length < 10) {
      alert('Description must be at least 10 characters long');
      return;
    }

    try {
      const result = await analyzeDescription(formData.description);
      alert(`AI Analysis:\n\n${result.analysis}`);
    } catch (err) {
      alert(`Error: ${err.response?.data?.detail || 'Failed to analyze description'}`);
    }
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">
        {item ? 'Edit Item' : 'Create New Item'}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Title Field with AI Assistant */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <div className="flex space-x-2">
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter item title"
            />
            <button
              type="button"
              onClick={handleGenerateTitle}
              disabled={aiLoading || !formData.description}
              className="px-3 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 transition-colors flex items-center"
              title="Generate title with AI"
            >
              <Wand2 size={16} />
            </button>
          </div>
        </div>

        {/* Description Field with AI Assistant */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <div className="space-y-2">
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="4"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter item description"
            />
            <button
              type="button"
              onClick={handleImproveDescription}
              disabled={aiLoading || !formData.description}
              className="text-sm px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50 transition-colors"
            >
              Improve with AI
            </button>
          </div>
        </div>

        {/* Price Field */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Price
          </label>
          <input
            type="number"
            name="price"
            value={formData.price}
            onChange={handleChange}
            step="0.01"
            min="0"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="0.00"
          />
        </div>

        {/* Form Actions */}
        <div className="flex justify-end space-x-3 pt-4">
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            {item ? 'Update' : 'Create'} Item
          </button>
        </div>
      </form>
    </div>
  );
};

export default ItemForm;
