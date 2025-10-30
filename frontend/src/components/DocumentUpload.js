import React, { useState, useCallback } from 'react';
import axios from 'axios';
import { Upload, FileText, CheckCircle, XCircle, Trash2, File } from 'lucide-react';

const DocumentUpload = ({ onDocumentUploaded, uploadedDocuments, onClearDocuments }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragOver(false);
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleFileUpload = async (file) => {
    // Validate file type
    const allowedTypes = ['.pdf', '.docx', '.txt'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedTypes.includes(fileExtension)) {
      setUploadStatus({
        type: 'error',
        message: `Unsupported file type. Please upload PDF, DOCX, or TXT files.`
      });
      return;
    }

    setIsUploading(true);
    setUploadStatus(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Do not set 'Content-Type' manually here — letting the browser
      // set it ensures the multipart boundary is included and the
      // server can parse the uploaded file correctly.
      const response = await axios.post('/api/upload', formData);

      setUploadStatus({
        type: 'success',
        message: `Successfully uploaded "${file.name}". ${response.data.chunks_created} chunks created.`
      });

      onDocumentUploaded({
        filename: response.data.filename,
        chunks: response.data.chunks_created,
        uploadTime: new Date().toLocaleTimeString()
      });

    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus({
        type: 'error',
        message: error.response?.data?.detail || 'Failed to upload document. Please try again.'
      });
    } finally {
      setIsUploading(false);
    }
  };

  const handleClearAll = async () => {
    try {
      await axios.delete('/api/documents');
      onClearDocuments();
      setUploadStatus({
        type: 'success',
        message: 'All documents cleared successfully.'
      });
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: 'Failed to clear documents.'
      });
    }
  };

  return (
    <div>
      {uploadStatus && (
        <div className={`status-message ${uploadStatus.type === 'success' ? 'status-success' : 'status-error'}`}>
          {uploadStatus.type === 'success' ? <CheckCircle size={20} /> : <XCircle size={20} />}
          {uploadStatus.message}
        </div>
      )}

      <div 
        className={`upload-area ${isDragOver ? 'dragover' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => document.getElementById('file-input').click()}
      >
        <input
          id="file-input"
          type="file"
          className="file-input"
          accept=".pdf,.docx,.txt"
          onChange={handleFileSelect}
          disabled={isUploading}
        />
        
        {isUploading ? (
          <div className="loading">
            <div className="spinner"></div>
            Uploading document...
          </div>
        ) : (
          <>
            <Upload className="upload-icon" size={48} />
            <div className="upload-text">
              Click to upload or drag and drop
            </div>
            <div className="upload-subtext">
              PDF, DOCX, or TXT files only
            </div>
          </>
        )}
      </div>

      {uploadedDocuments.length > 0 && (
        <div className="document-list">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
            <h4 style={{ margin: 0, color: '#2d3748' }}>Uploaded Documents ({uploadedDocuments.length})</h4>
            <button 
              onClick={handleClearAll}
              className="btn"
              style={{ 
                padding: '8px 16px', 
                fontSize: '0.9rem',
                background: 'linear-gradient(135deg, #e53e3e 0%, #c53030 100%)'
              }}
            >
              <Trash2 size={16} />
              Clear All
            </button>
          </div>
          
          {uploadedDocuments.map((doc, index) => (
            <div key={index} className="document-item">
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <FileText size={18} color="#667eea" />
                <div>
                  <div className="document-name">{doc.filename}</div>
                  <div className="document-info">
                    {doc.chunks} chunks • Uploaded at {doc.uploadTime}
                  </div>
                </div>
              </div>
              <File size={16} color="#64748b" />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;