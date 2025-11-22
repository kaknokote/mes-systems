import React, { useState } from 'react';
import { useItems } from '../hooks/useItems';
import { X, Loader } from 'lucide-react';

const AIAnalysisModal = ({ item, onClose }) => {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const { analyzeItem } = useItems();

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const result = await analyzeItem(item.id);
      setAnalysis(result);
    } catch (err) {
      // Error handled in hook
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex justify-between items-center p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold">AI Analysis</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {/* Item Info */}
          <div className="mb-6 p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold text-gray-800">{item.title}</h3>
            {item.description && (
              <p className="text-gray-600 mt-2">{item.description}</p>
            )}
          </div>

          {/* Analysis Button */}
          {!analysis && (
            <div className="text-center py-8">
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 transition-colors flex items-center mx-auto"
              >
                {loading && <Loader size={16} className="animate-spin mr-2" />}
                Analyze with AI
              </button>
              <p className="text-gray-500 mt-2 text-sm">
                Get AI-powered analysis and suggestions for this item
              </p>
            </div>
          )}

          {/* Analysis Results */}
          {analysis && (
            <div className="space-y-6">
              {/* Analysis */}
              <div>
                <h4 className="font-semibold text-gray-800 mb-3">Analysis</h4>
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <pre className="whitespace-pre-wrap text-sm text-blue-800">
                    {analysis.analysis}
                  </pre>
                </div>
              </div>

              {/* Generated Titles */}
              {analysis.generated_titles && (
                <div>
                  <h4 className="font-semibold text-gray-800 mb-3">
                    Suggested Titles
                  </h4>
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <pre className="whitespace-pre-wrap text-sm text-green-800">
                      {analysis.generated_titles}
                    </pre>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex justify-end p-6 border-t border-gray-200">
          <button
            onClick={onClose}
            className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default AIAnalysisModal;
