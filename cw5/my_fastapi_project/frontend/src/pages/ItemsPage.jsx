import React, { useState } from 'react';
import ItemList from '../components/ItemList';
import ItemForm from '../components/ItemForm';
import AIAnalysisModal from '../components/AIAnalysisModal';
import { useItems } from '../hooks/useItems';

const ItemsPage = () => {
  const [editingItem, setEditingItem] = useState(null);
  const [analyzingItem, setAnalyzingItem] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const { createItem, updateItem } = useItems();

  const handleFormSubmit = async (formData) => {
    try {
      if (editingItem) {
        await updateItem(editingItem.id, formData);
      } else {
        await createItem(formData);
      }
      setShowForm(false);
      setEditingItem(null);
    } catch (err) {
      // Error handled in hook
    }
  };

  const handleEdit = (item) => {
    setEditingItem(item);
    setShowForm(true);
  };

  const handleAnalyze = (item) => {
    setAnalyzingItem(item);
  };

  const handleCloseForm = () => {
    setShowForm(false);
    setEditingItem(null);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Items Management</h1>
        <p className="text-gray-600 mt-2">
          Manage your items with AI-powered assistance
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2">
          {showForm ? (
            <ItemForm
              item={editingItem}
              onSubmit={handleFormSubmit}
              onCancel={handleCloseForm}
            />
          ) : (
            <ItemList onEdit={handleEdit} onAnalyze={handleAnalyze} />
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Stats Card */}
          <div className="bg-white shadow-md rounded-lg p-6">
            <h3 className="font-semibold text-gray-800 mb-4">Quick Actions</h3>
            <div className="space-y-3">
              <button
                onClick={() => setShowForm(true)}
                className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-center"
              >
                Add New Item
              </button>
              <button
                onClick={() => window.location.href = '/chat'}
                className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-center"
              >
                Open AI Chat
              </button>
            </div>
          </div>

          {/* Info Card */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h4 className="font-semibold text-blue-800 mb-2">AI Features</h4>
            <ul className="text-blue-700 text-sm space-y-1">
              <li>• Generate titles with AI</li>
              <li>• Improve descriptions</li>
              <li>• Analyze item content</li>
              <li>• Get improvement suggestions</li>
            </ul>
          </div>
        </div>
      </div>

      {/* AI Analysis Modal */}
      {analyzingItem && (
        <AIAnalysisModal
          item={analyzingItem}
          onClose={() => setAnalyzingItem(null)}
        />
      )}
    </div>
  );
};

export default ItemsPage;
