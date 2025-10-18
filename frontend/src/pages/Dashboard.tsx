/**
 * Dashboard page component with file upload and work order management.
 */
import React, { useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { WorkOrder } from '@/types';
import Header from '@/components/layout/Header';
import FileUpload from '@/components/upload/FileUpload';
import WorkOrderList from '@/components/work-orders/WorkOrderList';
import ArtifactViewer from '@/components/work-orders/ArtifactViewer';

/**
 * Dashboard page with integrated file upload and work order tracking.
 */
const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [selectedWorkOrder, setSelectedWorkOrder] = useState<WorkOrder | null>(null);

  /**
   * Handle file upload completion.
   */
  const handleUploadComplete = (fileId: string, fileName: string) => {
    console.log('File uploaded:', fileId, fileName);
    // Trigger refresh of work orders list
    setRefreshTrigger((prev) => prev + 1);
  };

  /**
   * Handle work order selection.
   */
  const handleSelectWorkOrder = (workOrder: WorkOrder) => {
    setSelectedWorkOrder(workOrder);
  };

  /**
   * Close work order details.
   */
  const handleCloseDetails = () => {
    setSelectedWorkOrder(null);
  };

  return (
    <>
      <Header />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Message */}
        <div className="bg-gradient-to-r from-cfo-blue-deep to-cfo-blue-medium shadow-card rounded-card p-6 mb-8">
          <h1 className="text-title text-white">
            Welcome back, {user?.full_name || 'User'}!
          </h1>
          <p className="mt-2 text-body text-cfo-blue-sky">
            Upload your financial files to get AI-powered insights and forecasts
          </p>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - File Upload */}
          <div className="lg:col-span-1">
            <div className="bg-white shadow-card rounded-card p-6 sticky top-8">
              <h2 className="text-section text-cfo-neutral-dark mb-4">
                Upload Files
              </h2>
              <p className="text-body text-cfo-neutral-medium mb-4">
                Upload bank statements, trial balances, or other financial files for AI analysis
              </p>
              <FileUpload onUploadComplete={handleUploadComplete} />
            </div>
          </div>

          {/* Right Column - Work Orders */}
          <div className="lg:col-span-2">
            {selectedWorkOrder ? (
              <div className="bg-white shadow-card rounded-card p-6">
                {/* Work Order Details Header */}
                <div className="flex items-start justify-between mb-6">
                  <div>
                    <h2 className="text-title text-cfo-neutral-dark">
                      Work Order Details
                    </h2>
                    <p className="text-small text-cfo-neutral-medium mt-1">
                      ID: {selectedWorkOrder.id}
                    </p>
                  </div>
                  <button
                    onClick={handleCloseDetails}
                    className="text-gray-400 hover:text-cfo-neutral-medium transition-colors duration-200 ease-cfo"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>

                {/* Work Order Information */}
                <div className="bg-cfo-neutral-off-white rounded-card p-4 mb-6">
                  <h3 className="text-small font-medium text-cfo-neutral-medium mb-2">Objective</h3>
                  <p className="text-body text-cfo-neutral-dark">{selectedWorkOrder.objective || 'No objective specified'}</p>

                  <div className="grid grid-cols-2 gap-4 mt-4">
                    <div>
                      <h4 className="text-small font-medium text-cfo-neutral-medium">Status</h4>
                      <p className="text-body text-cfo-neutral-dark capitalize">{selectedWorkOrder.status}</p>
                    </div>
                    <div>
                      <h4 className="text-small font-medium text-cfo-neutral-medium">Created</h4>
                      <p className="text-body text-cfo-neutral-dark">
                        {new Date(selectedWorkOrder.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Agent Outputs */}
                {selectedWorkOrder.agent_outputs && Object.keys(selectedWorkOrder.agent_outputs).length > 0 && (
                  <div className="mb-6">
                    <h3 className="text-section text-cfo-neutral-dark mb-3">Agent Analysis</h3>
                    <div className="bg-cfo-blue-sky border border-cfo-blue-light rounded-card p-4">
                      <pre className="text-small text-cfo-neutral-dark whitespace-pre-wrap font-mono">
                        {JSON.stringify(selectedWorkOrder.agent_outputs, null, 2)}
                      </pre>
                    </div>
                  </div>
                )}

                {/* Artifacts */}
                {selectedWorkOrder.artifacts && selectedWorkOrder.artifacts.length > 0 && (
                  <ArtifactViewer artifacts={selectedWorkOrder.artifacts} />
                )}

                {/* No Results Yet */}
                {selectedWorkOrder.status === 'processing' && (
                  <div className="text-center py-8">
                    <svg
                      className="animate-spin h-12 w-12 text-cfo-blue-medium mx-auto mb-4"
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
                    <h3 className="text-section text-cfo-neutral-dark">Processing...</h3>
                    <p className="text-body text-cfo-neutral-medium mt-1">
                      Your files are being analyzed. This may take a few minutes.
                    </p>
                  </div>
                )}
              </div>
            ) : (
              <div className="bg-white shadow-card rounded-card p-6">
                <WorkOrderList
                  onSelectWorkOrder={handleSelectWorkOrder}
                  refreshTrigger={refreshTrigger}
                />
              </div>
            )}
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mt-8">
          <div className="bg-white shadow-card rounded-card p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-cfo-blue-sky rounded-button p-3">
                <svg className="h-6 w-6 text-cfo-blue-deep" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-small font-medium text-cfo-neutral-medium">Files Uploaded</h3>
                <p className="text-2xl font-bold text-cfo-neutral-dark">-</p>
              </div>
            </div>
          </div>

          <div className="bg-white shadow-card rounded-card p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-cfo-blue-sky rounded-button p-3">
                <svg className="h-6 w-6 text-cfo-blue-medium" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-small font-medium text-cfo-neutral-medium">Work Orders</h3>
                <p className="text-2xl font-bold text-cfo-neutral-dark">-</p>
              </div>
            </div>
          </div>

          <div className="bg-white shadow-card rounded-card p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-green-100 rounded-button p-3">
                <svg className="h-6 w-6 text-cfo-green" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-small font-medium text-cfo-neutral-medium">Completed</h3>
                <p className="text-2xl font-bold text-cfo-neutral-dark">-</p>
              </div>
            </div>
          </div>

          <div className="bg-white shadow-card rounded-card p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-cfo-blue-sky rounded-button p-3">
                <svg className="h-6 w-6 text-cfo-blue-deep" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-small font-medium text-cfo-neutral-medium">Artifacts</h3>
                <p className="text-2xl font-bold text-cfo-neutral-dark">-</p>
              </div>
            </div>
          </div>
        </div>

        {/* Help Text */}
        <div className="mt-8 bg-cfo-blue-sky border border-cfo-blue-light rounded-card p-6">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-cfo-blue-medium" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-small font-medium text-cfo-blue-deep">Getting Started</h3>
              <div className="mt-2 text-body text-cfo-blue-medium">
                <p>
                  Upload financial files like bank statements, trial balances, AR/AP reports, or P&L statements.
                  Our AI agents will analyze your data and generate insights, forecasts, and professional reports.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Dashboard;
