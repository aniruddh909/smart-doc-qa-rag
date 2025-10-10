import React, { useState } from 'react';
import axios from 'axios';
import { Send, AlertCircle } from 'lucide-react';

const QueryInterface = ({ onQuerySubmitted, hasDocuments, isLoading, setIsLoading }) => {
  const [query, setQuery] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a question.');
      return;
    }

    if (!hasDocuments) {
      setError('Please upload at least one document before asking questions.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/query', {
        query: query.trim(),
        k: 3
      });

      onQuerySubmitted(response.data);
      
    } catch (error) {
      console.error('Query error:', error);
      setError(error.response?.data?.detail || 'Failed to process your question. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      handleSubmit(e);
    }
  };

  const sampleQuestions = [
    "What is the main topic of the document?",
    "Can you summarize the key points?",
    "What are the important dates mentioned?",
    "Who are the main people or organizations mentioned?"
  ];

  const handleSampleClick = (sampleQuery) => {
    setQuery(sampleQuery);
    setError(null);
  };

  return (
    <div>
      {error && (
        <div className="status-message status-error">
          <AlertCircle size={20} />
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <textarea
          className="query-input"
          placeholder="Ask a question about your uploaded documents..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
          rows={4}
        />
        
        <button 
          type="submit" 
          className="btn"
          disabled={isLoading || !hasDocuments || !query.trim()}
        >
          {isLoading ? (
            <>
              <div className="spinner"></div>
              Processing...
            </>
          ) : (
            <>
              <Send size={16} />
              Ask Question
            </>
          )}
        </button>
      </form>

      {!hasDocuments && (
        <div style={{ 
          marginTop: '15px', 
          padding: '15px', 
          background: '#fff3cd', 
          border: '1px solid #ffeaa7', 
          borderRadius: '8px',
          color: '#856404'
        }}>
          <AlertCircle size={16} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
          Upload documents first to start asking questions.
        </div>
      )}

      {hasDocuments && !isLoading && (
        <div style={{ marginTop: '20px' }}>
          <h4 style={{ margin: '0 0 10px 0', color: '#64748b', fontSize: '0.9rem' }}>
            💡 Sample Questions:
          </h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {sampleQuestions.map((sample, index) => (
              <button
                key={index}
                type="button"
                onClick={() => handleSampleClick(sample)}
                style={{
                  background: '#f8fafc',
                  border: '1px solid #e2e8f0',
                  borderRadius: '6px',
                  padding: '8px 12px',
                  fontSize: '0.85rem',
                  color: '#64748b',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
                onMouseOver={(e) => {
                  e.target.style.background = '#eef2ff';
                  e.target.style.borderColor = '#667eea';
                  e.target.style.color = '#667eea';
                }}
                onMouseOut={(e) => {
                  e.target.style.background = '#f8fafc';
                  e.target.style.borderColor = '#e2e8f0';
                  e.target.style.color = '#64748b';
                }}
              >
                {sample}
              </button>
            ))}
          </div>
          <p style={{ 
            fontSize: '0.8rem', 
            color: '#a0aec0', 
            margin: '10px 0 0 0',
            fontStyle: 'italic'
          }}>
            Tip: Press Ctrl+Enter (or Cmd+Enter on Mac) to submit
          </p>
        </div>
      )}
    </div>
  );
};

export default QueryInterface;