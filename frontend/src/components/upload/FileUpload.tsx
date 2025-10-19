/**
 * FileUpload component with drag-and-drop functionality.
 */
import React, { useState, useCallback } from 'react';
import FileService from '@/services/fileService';
import Button from '@/components/common/Button';
import LoadingSpinner from '@/components/common/LoadingSpinner';

interface FileUploadProps {
  onUploadComplete?: (fileId: number, fileName: string, workOrderId?: number, datasetId?: number) => void;
  onWorkOrderCreated?: (workOrderId: number) => void;
  acceptedFileTypes?: string[];
  maxFileSizeMB?: number;
  showExecuteButton?: boolean; // Show manual execute button instead of auto-execute
}

/**
 * FileUpload component for uploading Excel/CSV files.
 */
const FileUpload: React.FC<FileUploadProps> = ({
  onUploadComplete,
  onWorkOrderCreated,
  acceptedFileTypes = ['.xlsx', '.xls', '.csv'],
  maxFileSizeMB = 100,
  showExecuteButton = false,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [workOrderId, setWorkOrderId] = useState<number | null>(null);
  const [isExecuting, setIsExecuting] = useState(false);

  /**
   * Validate file before upload.
   */
  const validateFile = (file: File): string | null => {
    // Check file size
    const maxSizeBytes = maxFileSizeMB * 1024 * 1024;
    if (file.size > maxSizeBytes) {
      return `File size exceeds ${maxFileSizeMB}MB limit`;
    }

    // Check file type
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!acceptedFileTypes.includes(fileExtension)) {
      return `Invalid file type. Accepted types: ${acceptedFileTypes.join(', ')}`;
    }

    return null;
  };

  /**
   * Handle file selection.
   */
  const handleFileSelect = useCallback((file: File) => {
    setError(null);
    setSuccess(null);

    const validationError = validateFile(file);
    if (validationError) {
      setError(validationError);
      return;
    }

    setSelectedFile(file);
  }, []);

  /**
   * Handle drag over event.
   */
  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  /**
   * Handle drag leave event.
   */
  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  /**
   * Handle file drop.
   */
  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  }, [handleFileSelect]);

  /**
   * Handle file input change.
   */
  const handleFileInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileSelect(files[0]);
    }
  }, [handleFileSelect]);

  /**
   * Upload the selected file.
   */
  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsUploading(true);
    setError(null);
    setSuccess(null);
    setUploadProgress(0);
    setWorkOrderId(null);

    try {
      const response = await FileService.uploadFile(selectedFile, (progressEvent) => {
        const progress = progressEvent.total
          ? Math.round((progressEvent.loaded * 100) / progressEvent.total)
          : 0;
        setUploadProgress(progress);
      });

      setSuccess(`File uploaded successfully: ${response.filename}`);
      setSelectedFile(null);
      setUploadProgress(0);

      // Debug: Log response
      console.log('Upload response:', response);
      console.log('Work order ID from response:', response.work_order_id);

      // Store work order ID if created
      if (response.work_order_id) {
        console.log('Setting work order ID:', response.work_order_id);
        setWorkOrderId(response.work_order_id);

        if (onWorkOrderCreated) {
          onWorkOrderCreated(response.work_order_id);
        }
      }

      if (onUploadComplete) {
        onUploadComplete(
          response.id,
          response.filename,
          response.work_order_id,
          response.dataset_id
        );
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload file. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  /**
   * Execute the work order (run Cash Commander).
   */
  const handleExecute = async () => {
    if (!workOrderId) return;

    setIsExecuting(true);
    setError(null);

    try {
      await FileService.executeWorkOrder(workOrderId);
      setSuccess(`Cash forecast completed! Work Order #${workOrderId} executed successfully.`);

      // Notify parent component
      if (onWorkOrderCreated) {
        onWorkOrderCreated(workOrderId);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to execute work order. Please try again.');
    } finally {
      setIsExecuting(false);
    }
  };

  /**
   * Clear selected file.
   */
  const handleClear = () => {
    setSelectedFile(null);
    setError(null);
    setSuccess(null);
    setUploadProgress(0);
  };

  return (
    <div className="w-full">
      {/* Drag and Drop Area */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center transition-colors
          ${isDragging
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 bg-white hover:border-gray-400'
          }
          ${selectedFile ? 'bg-green-50 border-green-300' : ''}
        `}
      >
        {!selectedFile ? (
          <>
            <div className="flex justify-center mb-4">
              <svg
                className="w-16 h-16 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Drop your file here, or click to browse
            </h3>
            <p className="text-sm text-gray-500 mb-4">
              Supported formats: {acceptedFileTypes.join(', ')} (Max {maxFileSizeMB}MB)
            </p>
            <input
              type="file"
              id="file-input"
              className="hidden"
              accept={acceptedFileTypes.join(',')}
              onChange={handleFileInputChange}
              disabled={isUploading}
              data-lpignore="true"
              data-form-type="other"
            />
            <label
              htmlFor="file-input"
              className="inline-block px-4 py-2 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors duration-200 cursor-pointer focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Browse Files
            </label>
          </>
        ) : (
          <>
            <div className="flex justify-center mb-4">
              <svg
                className="w-16 h-16 text-green-500"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {selectedFile.name}
            </h3>
            <p className="text-sm text-gray-500 mb-4">
              {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
            </p>
            <div className="flex justify-center space-x-3">
              <Button
                variant="primary"
                onClick={handleUpload}
                disabled={isUploading}
              >
                {isUploading ? 'Uploading...' : 'Upload File'}
              </Button>
              <Button
                variant="secondary"
                onClick={handleClear}
                disabled={isUploading}
              >
                Clear
              </Button>
            </div>
          </>
        )}
      </div>

      {/* Upload Progress */}
      {isUploading && uploadProgress > 0 && (
        <div className="mt-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Uploading...</span>
            <span className="text-sm font-medium text-gray-700">{uploadProgress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div
              className="bg-primary-600 h-2.5 rounded-full transition-all duration-300"
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          <div className="flex items-start">
            <svg
              className="w-5 h-5 mr-2 flex-shrink-0"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            </svg>
            <span>{error}</span>
          </div>
        </div>
      )}

      {/* Success Message */}
      {success && (
        <div className="mt-4 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
          <div className="flex items-start justify-between">
            <div className="flex items-start">
              <svg
                className="w-5 h-5 mr-2 flex-shrink-0"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clipRule="evenodd"
                />
              </svg>
              <span>{success}</span>
            </div>
            {showExecuteButton && workOrderId && !isExecuting && (
              <Button
                variant="primary"
                size="sm"
                onClick={handleExecute}
                className="ml-4"
              >
                Run Cash Forecast
              </Button>
            )}
          </div>
        </div>
      )}

      {/* Executing Status */}
      {isExecuting && (
        <div className="mt-4 bg-blue-50 border border-blue-200 text-blue-700 px-4 py-3 rounded">
          <div className="flex items-start">
            <svg
              className="w-5 h-5 mr-2 flex-shrink-0 animate-spin"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            <span>Running Cash Commander agent... This may take 30-60 seconds.</span>
          </div>
        </div>
      )}

      {/* Loading Indicator */}
      {isUploading && <LoadingSpinner text="Uploading file..." />}
    </div>
  );
};

export default FileUpload;
