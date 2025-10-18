/**
 * Service for file upload and work order management.
 */
import apiClient from './api';
import { FileUploadResponse, WorkOrder, Artifact } from '@/types';

/**
 * File service with methods for uploads, work orders, and artifacts.
 */
class FileService {
  /**
   * Upload a file to the server.
   * @param file - The file to upload
   * @param onProgress - Optional callback for upload progress
   * @returns Promise with upload response
   */
  async uploadFile(
    file: File,
    onProgress?: (progressEvent: ProgressEvent) => void
  ): Promise<FileUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.post<FileUploadResponse>(
      '/api/intake/upload',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: onProgress,
      }
    );

    return response.data;
  }

  /**
   * Get all work orders for the current user.
   * @returns Promise with array of work orders
   */
  async getWorkOrders(): Promise<WorkOrder[]> {
    const response = await apiClient.get<WorkOrder[]>('/api/work-orders');
    return response.data;
  }

  /**
   * Get a specific work order by ID.
   * @param workOrderId - The work order ID
   * @returns Promise with work order details
   */
  async getWorkOrder(workOrderId: string): Promise<WorkOrder> {
    const response = await apiClient.get<WorkOrder>(`/api/work-orders/${workOrderId}`);
    return response.data;
  }

  /**
   * Create a new work order from uploaded files.
   * @param objective - The objective/goal for the work order
   * @param fileIds - Array of uploaded file IDs
   * @returns Promise with created work order
   */
  async createWorkOrder(objective: string, fileIds: string[]): Promise<WorkOrder> {
    const response = await apiClient.post<WorkOrder>('/api/work-orders', {
      objective,
      input_datasets: fileIds,
    });
    return response.data;
  }

  /**
   * Download an artifact file.
   * @param artifactId - The artifact ID
   * @returns Promise with blob data
   */
  async downloadArtifact(artifactId: string): Promise<Blob> {
    const response = await apiClient.get(`/api/artifacts/${artifactId}/download`, {
      responseType: 'blob',
    });
    return response.data;
  }

  /**
   * Get artifact metadata.
   * @param artifactId - The artifact ID
   * @returns Promise with artifact details
   */
  async getArtifact(artifactId: string): Promise<Artifact> {
    const response = await apiClient.get<Artifact>(`/api/artifacts/${artifactId}`);
    return response.data;
  }
}

export default new FileService();
