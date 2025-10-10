import React, { useState } from 'react';
import DocumentUpload from './components/DocumentUpload';
import QueryInterface from './components/QueryInterface';
import ResultsDisplay from './components/ResultsDisplay';
import { BookOpen, MessageSquare } from 'lucide-react';

function App() {
  const [uploadedDocuments, setUploadedDocuments] = useState([]);
  const [queryResults, setQueryResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleDocumentUploaded = (documentInfo) => {
    setUploadedDocuments(prev => [...prev, documentInfo]);
  };

  const handleQuerySubmitted = async (results) => {
    setQueryResults(results);
  };

  const handleClearDocuments = () => {
    setUploadedDocuments([]);
    setQueryResults(null);
  };

  return (
    <div className="container">
      <header className="header">
        <h1>🤖 Smart Document Q&A</h1>
        <p>Upload documents and ask questions using AI-powered Retrieval Augmented Generation</p>
      </header>

      <div className="main-content">
        <div className="upload-section">
          <h2 className="section-title">
            <BookOpen size={24} />
            Document Upload
          </h2>
          <DocumentUpload 
            onDocumentUploaded={handleDocumentUploaded}
            uploadedDocuments={uploadedDocuments}
            onClearDocuments={handleClearDocuments}
          />
        </div>

        <div className="query-section">
          <h2 className="section-title">
            <MessageSquare size={24} />
            Ask Questions
          </h2>
          <QueryInterface 
            onQuerySubmitted={handleQuerySubmitted}
            hasDocuments={uploadedDocuments.length > 0}
            isLoading={isLoading}
            setIsLoading={setIsLoading}
          />
        </div>
      </div>

      {queryResults && (
        <ResultsDisplay 
          results={queryResults}
          isLoading={isLoading}
        />
      )}
    </div>
  );
}

export default App;