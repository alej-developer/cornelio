"use client";

import type { QueryResponse } from "@/types";
import { useTranslation } from "@/context/LanguageContext";
import styles from "./ResponseViewer.module.css";

interface ResponseViewerProps {
  response: QueryResponse | null;
  loading: boolean;
  error: string | null;
}

export default function ResponseViewer({ response, loading, error }: ResponseViewerProps) {
  const { t } = useTranslation();

  if (loading) {
    return (
      <div className={styles.viewer}>
        <div className={styles.pulseContainer}>
          <div className={styles.pulse} />
          <div className={styles.pulse} />
          <div className={styles.pulse} />
        </div>
      </div>
    );
  }

  if (!response) {
    return (
      <div className={styles.viewer}>
        <div className={styles.empty}>
          {t("consultas.no_response")}
        </div>
      </div>
    );
  }

  return (
    <div className={styles.viewer}>
      <div className={styles.content}>
        <p className={styles.answer}>{response.answer}</p>
      </div>

      <div className={styles.meta}>
        <span className={styles.latency}>
          {t("consultas.latency")} {response.latency_ms.toFixed(0)}ms
        </span>
        <div className={styles.confidence}>
          <span>{t("consultas.confidence")}</span>
          <div className={styles.confidenceBar}>
            <div
              className={styles.confidenceFill}
              style={{ width: `${(response.sources[0]?.relevance_score || 0.8) * 100}%` }}
            />
          </div>
        </div>
      </div>

      {response.sources.length > 0 && (
        <div className={styles.sourcesContainer}>
          <h4 className={styles.sourcesTitle}>{t("consultas.sources")}</h4>
          <ul className={styles.sourcesList}>
            {response.sources.map((source, idx) => (
              <li key={idx} className={styles.sourceItem}>
                <span className={styles.sourceName}>{source.filename}</span>
                <span className={styles.sourceRelevance}>
                  {(source.relevance_score * 100).toFixed(0)}%
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
