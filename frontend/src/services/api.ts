/**
 * Base API client for Cornelio.
 *
 * All requests go through this module to guarantee:
 * - Consistent error handling and sanitization
 * - Request timeouts via AbortController
 * - Typed responses
 */

import { ApiError, handleFetchError } from "@/lib/errors";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const DEFAULT_TIMEOUT_MS = 30_000;
const UPLOAD_TIMEOUT_MS = 60_000;

interface RequestConfig {
  method?: string;
  body?: unknown;
  headers?: Record<string, string>;
  timeout?: number;
}

async function request<T>(endpoint: string, config: RequestConfig = {}): Promise<T> {
  const {
    method = "GET",
    body,
    headers = {},
    timeout = DEFAULT_TIMEOUT_MS,
  } = config;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);

  const init: RequestInit = {
    method,
    signal: controller.signal,
    headers: {
      "Content-Type": "application/json",
      ...headers,
    },
  };

  if (body !== undefined && method !== "GET") {
    init.body = JSON.stringify(body);
  }

  try {
    const res = await fetch(`${BASE_URL}${endpoint}`, init);
    clearTimeout(timer);

    if (!res.ok) {
      let msg = "";
      try {
        const data = await res.json();
        msg = data.error || data.detail || "";
      } catch {
        /* response body not JSON */
      }
      throw new ApiError(res.status, msg);
    }

    return (await res.json()) as T;
  } catch (err) {
    clearTimeout(timer);
    if (err instanceof ApiError) throw err;
    throw new ApiError(0, handleFetchError(err));
  }
}

async function upload<T>(endpoint: string, file: File): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), UPLOAD_TIMEOUT_MS);

  const form = new FormData();
  form.append("file", file);

  try {
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      method: "POST",
      body: form,
      signal: controller.signal,
    });
    clearTimeout(timer);

    if (!res.ok) {
      let msg = "";
      try {
        const data = await res.json();
        msg = data.error || "";
      } catch {
        /* non-JSON error body */
      }
      throw new ApiError(res.status, msg);
    }

    return (await res.json()) as T;
  } catch (err) {
    clearTimeout(timer);
    if (err instanceof ApiError) throw err;
    throw new ApiError(0, handleFetchError(err));
  }
}

export const api = {
  get: <T>(endpoint: string) => request<T>(endpoint),
  post: <T>(endpoint: string, body: unknown) =>
    request<T>(endpoint, { method: "POST", body }),
  upload: <T>(endpoint: string, file: File) => upload<T>(endpoint, file),
};
