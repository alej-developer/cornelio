/**
 * Capa de servicio tipada — mapea a los endpoints de FastAPI.
 */

import { api } from "./api";
import type {
  InferenceRequest,
  InferenceResponse,
  QueryRequest,
  QueryResponse,
  DocumentUploadResponse,
  ReportResponse,
  ReadinessResponse,
} from "@/types";

export const inferenceService = {
  generate: (data: InferenceRequest): Promise<InferenceResponse> =>
    api.post<InferenceResponse>("/api/v1/inference/generate", data),
};

export const queryService = {
  query: (data: QueryRequest): Promise<QueryResponse> =>
    api.post<QueryResponse>("/api/v1/query", data),
};

export const documentService = {
  upload: (file: File): Promise<DocumentUploadResponse> =>
    api.upload<DocumentUploadResponse>("/api/v1/documents/upload", file),
};

export const reportService = {
  generate: (): Promise<ReportResponse> =>
    api.get<ReportResponse>("/api/v1/reports/generate"),
};

export const systemService = {
  readiness: (): Promise<ReadinessResponse> =>
    api.get<ReadinessResponse>("/readiness"),
  health: (): Promise<{ status: string }> =>
    api.get<{ status: string }>("/health"),
};
