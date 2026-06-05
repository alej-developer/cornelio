/**
 * TypeScript type definitions for the Cornelio frontend.
 *
 * API types mirror the backend Pydantic schemas exactly.
 * UI types are frontend-specific and used for state management.
 */

// ---------------------------------------------------------------------------
// API Request Types
// ---------------------------------------------------------------------------

export interface InferenceRequest {
  prompt: string;
  max_tokens?: number;
  temperature?: number;
}

export interface QueryRequest {
  query: string;
  max_results?: number;
  temperature?: number;
  max_tokens?: number;
}

// ---------------------------------------------------------------------------
// API Response Types
// ---------------------------------------------------------------------------

export interface InferenceResponse {
  text: string;
  model: string;
  tokens_generated: number;
  latency_ms: number;
}

export interface SourceDocument {
  content: string;
  filename: string;
  relevance_score: number;
}

export interface QueryResponse {
  answer: string;
  sources: SourceDocument[];
  model: string;
  latency_ms: number;
}

export interface DocumentUploadResponse {
  document_id: string;
  filename: string;
  chunks_created: number;
  status: string;
}

export interface ReportSection {
  heading: string;
  body: string;
}

export interface ReportResponse {
  report_id: string;
  title: string;
  summary: string;
  sections: ReportSection[];
  document_count: number;
  generated_at: string;
}

export interface ReadinessResponse {
  status: string;
  mlx_model_loaded: boolean;
  vector_store_ready: boolean;
}

export interface ApiErrorResponse {
  error: string;
}

// ---------------------------------------------------------------------------
// UI Types
// ---------------------------------------------------------------------------

export type NotificationType = "success" | "error" | "warning" | "info";

export interface Notification {
  id: string;
  type: NotificationType;
  message: string;
}

export type TaskStatus = "pending" | "running" | "completed" | "failed";

export interface AutomatedTask {
  id: string;
  name: string;
  status: TaskStatus;
  description: string;
  lastRun: string | null;
}
