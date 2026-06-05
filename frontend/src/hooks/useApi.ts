"use client";

/**
 * Generic hook for managing API call state (loading, data, error).
 *
 * Uses useReducer for predictable state transitions.
 * All errors are sanitized before reaching component state.
 */

import { useCallback, useReducer } from "react";
import { ApiError, handleFetchError } from "@/lib/errors";

interface ApiState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

type ApiAction<T> =
  | { type: "LOADING" }
  | { type: "SUCCESS"; payload: T }
  | { type: "ERROR"; payload: string }
  | { type: "RESET" };

function reducer<T>(state: ApiState<T>, action: ApiAction<T>): ApiState<T> {
  switch (action.type) {
    case "LOADING":
      return { data: state.data, loading: true, error: null };
    case "SUCCESS":
      return { data: action.payload, loading: false, error: null };
    case "ERROR":
      return { data: state.data, loading: false, error: action.payload };
    case "RESET":
      return { data: null, loading: false, error: null };
  }
}

export function useApi<T>() {
  const [state, dispatch] = useReducer(reducer<T>, {
    data: null,
    loading: false,
    error: null,
  });

  const execute = useCallback(
    async (call: () => Promise<T>): Promise<T | null> => {
      dispatch({ type: "LOADING" });
      try {
        const result = await call();
        dispatch({ type: "SUCCESS", payload: result });
        return result;
      } catch (err) {
        const message =
          err instanceof ApiError ? err.userMessage : handleFetchError(err);
        dispatch({ type: "ERROR", payload: message });
        return null;
      }
    },
    [],
  );

  const reset = useCallback(() => dispatch({ type: "RESET" }), []);

  return { ...state, execute, reset };
}
