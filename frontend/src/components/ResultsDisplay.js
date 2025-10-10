import React, { useState } from 'react';
import { MessageCircle, FileText, Copy, Check } from 'lucide-react';

const ResultsDisplay = ({ results, isLoading }) => {
  const [activeTab, setActiveTab] = useState('answer');
  const [copiedAnswer, setCopiedAnswer] = useState(false);

  const handleCopyAnswer = async () => {
    try {
      await navigator.clipboard.writeText(results.answer);
      setCopiedAnswer(true);
      setTimeout(() => setCopiedAnswer(false), 2000);
    } catch (err) {
      console.error('Failed to copy text:', err);
    }
  };

  if (isLoading) {
    return (
      <div className="results-section">
        <div className="loading">
          <div className="spinner"></div>
          Generating AI answer from your documents...
        </div>
      </div>
    );
  }

  if (!results) {
    return null;
  }

  return (
    <div className="results-section">
      <div className="results-tabs">
        <button 
          className={`tab ${activeTab === 'answer' ? 'active' : ''}`}
          onClick={() => setActiveTab('answer')}
        >
          <MessageCircle size={18} style={{ marginRight: '8px' }} />
          AI Answer
        </button>
        <button 
          className={`tab ${activeTab === 'context' ? 'active' : ''}`}
          onClick={() => setActiveTab('context')}
        >
          <FileText size={18} style={{ marginRight: '8px' }} />
          Context & Sources
        </button>
      </div>

      <div className="results-content">
        {activeTab === 'answer' && (
          <div className="answer-section">
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'flex-start',
              marginBottom: '15px'
            }}>
              <h3 style={{ 
                margin: 0, 
                color: '#2d3748',
                display: 'flex',
                alignItems: 'center',
                gap: '10px'
              }}>
                <MessageCircle size={20} color="#667eea" />
                Answer for: "{results.query}"
              </h3>
              <button
                onClick={handleCopyAnswer}
                className="btn"
                style={{
                  padding: '8px 12px',
                  fontSize: '0.8rem',
                  background: copiedAnswer ? '#38a169' : '#4a5568'
                }}
              >
                {copiedAnswer ? <Check size={14} /> : <Copy size={14} />}
                {copiedAnswer ? 'Copied!' : 'Copy'}
              </button>
            </div>
            
            <div className="answer-text">
              {results.answer}
            </div>

            {results.sources && results.sources.length > 0 && (
              <div style={{ marginTop: '20px' }}>
                <h4 style={{ color: '#4a5568', marginBottom: '10px' }}>
                  📊 Found {results.sources.length} relevant sources
                </h4>
                <div style={{ 
                  display: 'flex', 
                  gap: '10px', 
                  flexWrap: 'wrap'
                }}>
                  {results.sources.map((source, index) => (
                    <div
                      key={index}
                      style={{
                        background: '#f0f9ff',
                        border: '1px solid #0ea5e9',
                        borderRadius: '6px',
                        padding: '8px 12px',
                        fontSize: '0.85rem',
                        color: '#0369a1'
                      }}
                    >
                      📄 {source.source} (Chunk {source.chunk_id + 1})
                      <br />
                      <span style={{ fontSize: '0.75rem', opacity: 0.8 }}>
                        Similarity: {(1 - source.similarity_score).toFixed(3)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'context' && (
          <div className="context-section">
            <h3 style={{ 
              margin: '0 0 15px 0', 
              color: '#2d3748',
              display: 'flex',
              alignItems: 'center',
              gap: '10px'
            }}>
              <FileText size={20} color="#667eea" />
              Retrieved Context
            </h3>
            
            <div className="context-text">
              {results.context}
            </div>

            {results.sources && results.sources.length > 0 && (
              <div className="sources-section">
                <h4 style={{ color: '#4a5568', marginBottom: '15px' }}>
                  📚 Source Details
                </h4>
                
                {results.sources.map((source, index) => (
                  <div key={index} className="source-item">
                    <div className="source-header">
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <FileText size={16} color="#667eea" />
                        <strong>{source.source}</strong>
                        <span style={{ 
                          fontSize: '0.8rem', 
                          background: '#e2e8f0', 
                          padding: '2px 6px', 
                          borderRadius: '4px' 
                        }}>
                          Chunk {source.chunk_id + 1}
                        </span>
                      </div>
                      <div style={{ 
                        fontSize: '0.8rem', 
                        background: source.similarity_score < 0.5 ? '#dcfce7' : '#fef3c7',
                        color: source.similarity_score < 0.5 ? '#166534' : '#92400e',
                        padding: '2px 6px',
                        borderRadius: '4px'
                      }}>
                        {source.similarity_score < 0.5 ? '🟢 High' : '🟡 Medium'} Relevance
                      </div>
                    </div>
                    <div className="source-preview">
                      "{source.preview}"
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsDisplay;