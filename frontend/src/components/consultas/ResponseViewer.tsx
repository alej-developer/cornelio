"use client";

import { useState } from "react";
import type { QueryResponse } from "@/types";
import styles from "./ResponseViewer.module.css";

interface ResponseViewerProps {
  response: QueryResponse | null;
  loading: boolean;
  error: string | null;
}

export default function ResponseViewer({
  response,
  loading,
  error,
}: ResponseViewerProps) {
  const [expandedSource, setExpandedSource] = useState<number | null>(null);

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.skeleton}>
          <div className={styles.skeletonLine} style={{ width: "90%" }} />
          <div className={styles.skeletonLine} style={{ width: "75%" }} />
          <div className={styles.skeletonLine} style={{ width: "60%" }} />
          <div className={styles.skeletonLine} style={{ width: "80%" }} />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.container}>
        <div className={styles.errorBanner}>{error}</div>
      </div>
    );
  }

  if (!response) {
    return (
      <div className={styles.container}>
        <div className={styles.empty}>
          <svg width="40" height="40" viewBox="0 0 40 40" fill="none" stroke="var(--text-muted)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="20" cy="20" r="16" />
            <line x1="20" y1="12" x2="20" y2="22" />
            <circle cx="20" cy="27" r="1" fill="var(--text-muted)" />
          </svg>
          <p>Submit a query to see results here.</p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.answer}>
        <h3 className={styles.answerLabel}>Response</h3>
        <p className={styles.answerText}>{response.answer}</p>
        <div className={styles.answerMeta}>
          <span>Model: {response.model}</span>
          <span>Latency: {response.latency_ms.toFixed(0)}ms</span>
        </div>
      </div>

      {response.sources.length > 0 && (
        <div className={styles.sources}>
          <h4 className={styles.sourcesLabel}>
            Sources ({response.sources.length})
          </h4>
          {response.sources.map((source, i) => (
            <div key={i} className={styles.source}>
              <button
                className={styles.sourceHeader}
                onClick={() =>
                  setExpandedSource(expandedSource === i ? null : i)
                }
              >
                <div className={styles.sourceInfo}>
                  <span className={styles.sourceFile}>{source.filename}</span>
                  <span className={styles.sourceScore}>
                    {(source.relevance_score * 100).toFixed(0)}% match
                  </span>
                </div>
                <span className={styles.chevron}>
                  {expandedSource === i ? "\u2212" : "+"}
                </span>
              </button>
              {expandedSource === i && (
                <div className={styles.sourceContent}>
                  <pre>{source.content}</pre>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
