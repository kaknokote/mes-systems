import React, { useState } from 'react';
import { useItems } from '../hooks/useItems';
import { Plus, Search, Edit, Trash2, Brain } from 'lucide-react';

const ItemList = ({ onEdit, onAnalyze }) => {
  const { items, loading, error, deleteItem, fetchItems } = useItems();
  const [searchTerm, setSearchTerm] = useState('');
  const [deletingId, setDeletingId] = useState(null);

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    fetchItems(0, 100, e.target.value);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this item?')) return;
    
    setDeletingId(id);
    try {
      await deleteItem(id);
    } catch (err) {
      // Error handled in hook
    } finally {
      setDeletingId(null);
    }
  };

  if (loading && items.length === 0) {
    return (
      <div className="flex justify-center items-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="bg-white shadow-md rounded-lg overflow-hidden">
      {/* Header with Search */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-800">Items</h2>
          <button
            onClick={() => onEdit(null)}
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus size={16} className="mr-2" />
            Add Item
          </button>
        </div>
        
        <div className="relative">
          <Search size={20} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Search items by title..."
            value={searchTerm}
            onChange={handleSearch}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="m-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Items List */}
      <div className="divide-y divide-gray-200">
        {items.map((item) => (
          <div key={item.id} className="p-4 hover:bg-gray-50 transition-colors">
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <h3 className="font-semibold text-gray-800">{item.title}</h3>
                {item.description && (
                  <p className="text-gray-600 mt-1 text-sm">{item.description}</p>
                )}
                {item.price && (
                  <p className="text-green-600 font-medium mt-1">${item.price}</p>
                )}
              </div>
              
              <div className="flex space-x-2 ml-4">
                <button
                  onClick={() => onAnalyze(item)}
                  className="p-2 text-purple-600 hover:bg-purple-50 rounded-lg transition-colors"
                  title="Analyze with AI"
                >
                  <Brain size={16} />
                </button>
                <button
                  onClick={() => onEdit(item)}
                  className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                  title="Edit"
                >
                  <Edit size={16} />
                </button>
                <button
                  onClick={() => handleDelete(item.id)}
                  disabled={deletingId === item.id}
                  className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50"
                  title="Delete"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {items.length === 0 && !loading && (
        <div className="p-8 text-center text-gray-500">
          <p>No items found. Create your first item!</p>
        </div>
      )}
    </div>
  );
};

export default ItemList;
