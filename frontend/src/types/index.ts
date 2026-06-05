/**
 * [ES] Definiciones de tipos TypeScript para el frontend de Cornelio. / [EN] TypeScript type definitions for the Cornelio frontend.
 *
 * [ES] Los tipos de la API reflejan exactamente los esquemas Pydantic del backend. / [EN] API types exactly mirror backend Pydantic schemas.
 * [ES] Los tipos UI son específicos del frontend y se usan para la gestión del estado. / [EN] UI types are frontend-specific and used for state management.
 */

// ---------------------------------------------------------------------------
// [ES] Tipos de Solicitud API / [EN] API Request Types
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
// [ES] Tipos de Respuesta API / [EN] API Response Types
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
// [ES] Tipos UI / [EN] UI Types
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
