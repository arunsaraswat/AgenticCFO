/**
 * TypeScript type definitions for the application.
 */

/**
 * User interface representing a user in the system.
 */
export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
}

/**
 * Extended user profile with additional information.
 */
export interface UserProfile extends User {
  updated_at: string;
  is_superuser: boolean;
}

/**
 * Login request payload.
 */
export interface LoginRequest {
  email: string;
  password: string;
}

/**
 * Login response with JWT token.
 */
export interface LoginResponse {
  access_token: string;
  token_type: string;
}

/**
 * Registration request payload.
 */
export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
}

/**
 * Registration response.
 */
export interface RegisterResponse {
  id: number;
  email: string;
  full_name: string;
  message: string;
}

/**
 * Dashboard data interface.
 */
export interface DashboardData {
  user: User;
  stats: Record<string, number>;
  message: string;
}

/**
 * API error response structure.
 */
export interface ApiError {
  detail: string;
}

/**
 * Authentication context value.
 */
export interface AuthContextValue {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string) => Promise<void>;
  logout: () => void;
}

/**
 * Work Order status types.
 */
export type WorkOrderStatus = 'pending' | 'processing' | 'completed' | 'failed';

/**
 * Work Order interface.
 */
export interface WorkOrder {
  id: number;
  tenant_id: number;
  objective: string;
  status: WorkOrderStatus;
  progress_percentage: number;
  current_agent?: string | null;
  input_datasets: number[];
  policy_refs: string[];
  agent_outputs: Record<string, any>;
  guardrail_checks: any[];
  approval_gates: any[];
  artifacts: ArtifactSummary[];
  execution_log: any[];
  error_message?: string | null;
  total_cost_usd: number;
  execution_time_seconds?: number | null;
  created_by_user_id?: number | null;
  created_at: string;
  updated_at: string;
  completed_at?: string | null;
}

/**
 * Artifact summary (simplified version stored in work order).
 */
export interface ArtifactSummary {
  artifact_type: string;
  artifact_name: string;
  file_size_bytes: number;
}

/**
 * Full artifact interface with all details.
 */
export interface Artifact {
  id: number;
  work_order_id: number;
  artifact_type: string;
  artifact_name: string;
  file_path: string;
  checksum_sha256: string;
  file_size_bytes: number;
  mime_type?: string | null;
  artifact_metadata: Record<string, any>;
  generated_by_agent?: string | null;
  created_at: string;
}

/**
 * File upload response.
 */
export interface FileUploadResponse {
  id: number;
  tenant_id: number;
  filename: string;
  file_hash: string;
  file_size_bytes: number;
  mime_type?: string | null;
  workbook_risk_score?: number | null;
  security_scan_results?: any;
  status: string;
  error_message?: string | null;
  uploaded_by_user_id?: number | null;
  created_at: string;
  work_order_id?: number | null;
  dataset_id?: number | null;
}
