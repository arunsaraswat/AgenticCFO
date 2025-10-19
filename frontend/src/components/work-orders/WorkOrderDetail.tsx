/**
 * WorkOrderDetail component for displaying work order execution details.
 */
import React, { useState, useEffect } from 'react';
import FileService from '@/services/fileService';
import { WorkOrder, Artifact } from '@/types';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import Button from '@/components/common/Button';
import CashCommanderResults from './CashCommanderResults';
import { formatCurrency, formatDuration } from '@/utils/format';

interface WorkOrderDetailProps {
  workOrderId: number;
  autoRefresh?: boolean; // Auto-refresh while processing
  refreshInterval?: number; // Refresh interval in ms
}

/**
 * WorkOrderDetail component showing work order status, progress, and artifacts.
 */
const WorkOrderDetail: React.FC<WorkOrderDetailProps> = ({
  workOrderId,
  autoRefresh = true,
  refreshInterval = 3000,
}) => {
  const [workOrder, setWorkOrder] = useState<WorkOrder | null>(null);
  const [artifacts, setArtifacts] = useState<Artifact[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isDownloading, setIsDownloading] = useState<number | null>(null);

  /**
   * Fetch work order details.
   */
  const fetchWorkOrder = async () => {
    try {
      const data = await FileService.getWorkOrder(workOrderId);
      setWorkOrder(data);

      // Fetch artifacts if work order is completed
      if (data.status === 'completed' && data.artifacts.length > 0) {
        const artifactList = await FileService.getWorkOrderArtifacts(workOrderId);
        setArtifacts(artifactList);
      }

      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load work order');
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Download an artifact.
   */
  const handleDownload = async (artifact: Artifact) => {
    setIsDownloading(artifact.id);
    try {
      await FileService.downloadArtifact(artifact.id, artifact.artifact_name);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to download artifact');
    } finally {
      setIsDownloading(null);
    }
  };

  /**
   * Execute work order.
   */
  const handleExecute = async () => {
    try {
      setIsLoading(true);
      await FileService.executeWorkOrder(workOrderId);
      await fetchWorkOrder(); // Refresh after execution
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to execute work order');
      setIsLoading(false);
    }
  };

  // Initial load
  useEffect(() => {
    fetchWorkOrder();
  }, [workOrderId]);

  // Auto-refresh while processing
  useEffect(() => {
    if (!autoRefresh || !workOrder) return;

    if (workOrder.status === 'processing' || workOrder.status === 'pending') {
      const interval = setInterval(fetchWorkOrder, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [workOrder?.status, autoRefresh, refreshInterval]);

  /**
   * Get status badge color.
   */
  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'processing':
        return 'bg-blue-100 text-blue-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'pending':
      default:
        return 'bg-yellow-100 text-yellow-800';
    }
  };

  /**
   * Get status icon.
   */
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
              clipRule="evenodd"
            />
          </svg>
        );
      case 'processing':
        return (
          <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
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
        );
      case 'failed':
        return (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clipRule="evenodd"
            />
          </svg>
        );
      default:
        return (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
              clipRule="evenodd"
            />
          </svg>
        );
    }
  };

  /**
   * Generate and download Excel artifact.
   */
  const handleDownloadExcel = async () => {
    if (!artifacts || artifacts.length === 0) {
      setError('No artifacts available to download');
      return;
    }

    try {
      // Find the first Excel artifact
      const excelArtifact = artifacts.find(a => a.artifact_type === 'excel');

      if (!excelArtifact) {
        setError('No Excel artifact found');
        return;
      }

      // Download the artifact
      await FileService.downloadArtifact(excelArtifact.id, excelArtifact.artifact_name);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to download Excel artifact');
    }
  };

  if (isLoading && !workOrder) {
    return <LoadingSpinner text="Loading work order..." />;
  }

  if (error && !workOrder) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        <div className="flex items-start">
          <svg className="w-5 h-5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clipRule="evenodd"
            />
          </svg>
          <span>{error}</span>
        </div>
      </div>
    );
  }

  if (!workOrder) return null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              {workOrder.objective}
            </h2>
            <p className="text-sm text-gray-500">
              Work Order #{workOrder.id} • Created{' '}
              {new Date(workOrder.created_at).toLocaleString()}
            </p>
          </div>
          <span
            className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(
              workOrder.status
            )}`}
          >
            <span className="mr-2">{getStatusIcon(workOrder.status)}</span>
            {workOrder.status.charAt(0).toUpperCase() + workOrder.status.slice(1)}
          </span>
        </div>

        {/* Progress Bar */}
        {(workOrder.status === 'processing' || workOrder.status === 'pending') && (
          <div className="mb-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">
                {workOrder.current_agent ? `Running: ${workOrder.current_agent}` : 'Initializing...'}
              </span>
              <span className="text-sm font-medium text-gray-700">{workOrder.progress_percentage}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
                style={{ width: `${workOrder.progress_percentage}%` }}
              />
            </div>
          </div>
        )}

        {/* Execute Button (if pending) */}
        {workOrder.status === 'pending' && (
          <div className="mb-4">
            <Button variant="primary" onClick={handleExecute} disabled={isLoading}>
              Run Cash Commander
            </Button>
          </div>
        )}

        {/* Error Message */}
        {workOrder.error_message && (
          <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            <p className="font-medium">Execution Error:</p>
            <p className="text-sm">{workOrder.error_message}</p>
          </div>
        )}

        {/* Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-500">Execution Time</p>
            <p className="text-lg font-semibold text-gray-900">
              {workOrder.execution_time_seconds
                ? formatDuration(workOrder.execution_time_seconds)
                : '—'}
            </p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-500">Total Cost</p>
            <p className="text-lg font-semibold text-gray-900">
              {formatCurrency(workOrder.total_cost_usd, 4)}
            </p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-500">Artifacts</p>
            <p className="text-lg font-semibold text-gray-900">
              {workOrder.artifacts.length}
            </p>
          </div>
        </div>
      </div>

      {/* Cash Commander Results (if completed) */}
      {workOrder.status === 'completed' &&
        workOrder.agent_outputs &&
        workOrder.agent_outputs.cash_commander && (
          <div className="bg-white shadow rounded-lg p-6">
            <CashCommanderResults
              output={workOrder.agent_outputs.cash_commander.output}
              workOrderId={workOrder.id}
              onDownloadExcel={handleDownloadExcel}
            />
          </div>
        )}

      {/* Artifacts */}
      {artifacts.length > 0 && (
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Generated Artifacts</h3>
          <div className="space-y-3">
            {artifacts.map((artifact) => (
              <div
                key={artifact.id}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center space-x-3">
                  <svg className="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fillRule="evenodd"
                      d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z"
                      clipRule="evenodd"
                    />
                  </svg>
                  <div>
                    <p className="font-medium text-gray-900">{artifact.artifact_name}</p>
                    <p className="text-sm text-gray-500">
                      {artifact.artifact_type.toUpperCase()} • {artifact.file_size_bytes} bytes •{' '}
                      {artifact.generated_by_agent || 'Unknown agent'}
                    </p>
                  </div>
                </div>
                <Button
                  variant="primary"
                  size="sm"
                  onClick={() => handleDownload(artifact)}
                  disabled={isDownloading === artifact.id}
                >
                  {isDownloading === artifact.id ? 'Downloading...' : 'Download'}
                </Button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Debug: Agent Outputs (collapsed by default) */}
      {workOrder.status === 'completed' && workOrder.agent_outputs && Object.keys(workOrder.agent_outputs).length > 0 && (
        <details className="bg-white shadow rounded-lg p-6">
          <summary className="cursor-pointer text-sm font-medium text-gray-700 hover:text-gray-900">
            🔍 View Technical Details (Debug Info)
          </summary>
          <div className="mt-4 space-y-4">
            {Object.entries(workOrder.agent_outputs).map(([agentName, output]: [string, any]) => (
              <div key={agentName} className="bg-gray-50 p-4 rounded-lg">
                <h4 className="font-medium text-gray-900 mb-2">
                  {agentName.replace('_', ' ').toUpperCase()}
                </h4>
                {output.confidence_score && (
                  <p className="text-sm text-gray-600 mb-2">
                    Confidence Score: {(output.confidence_score * 100).toFixed(0)}%
                  </p>
                )}
                {output.reasoning_trace && output.reasoning_trace.length > 0 && (
                  <div className="mt-2">
                    <p className="text-xs font-medium text-gray-700 mb-1">Reasoning Trace:</p>
                    <ul className="list-disc list-inside space-y-1">
                      {output.reasoning_trace.slice(0, 10).map((trace: string, idx: number) => (
                        <li key={idx} className="text-xs text-gray-600">
                          {trace}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </details>
      )}
    </div>
  );
};

export default WorkOrderDetail;
