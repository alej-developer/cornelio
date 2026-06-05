"use client";

import { useState } from "react";
import Button from "@/components/ui/Button";
import styles from "./QueryForm.module.css";

interface QueryFormProps {
  onSubmit: (query: string, maxResults: number, temperature: number) => void;
  loading: boolean;
}

export default function QueryForm({ onSubmit, loading }: QueryFormProps) {
  const [query, setQuery] = useState("");
  const [maxResults, setMaxResults] = useState(5);
  const [temperature, setTemperature] = useState(0.7);
  const [showParams, setShowParams] = useState(false);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (query.trim()) {
      onSubmit(query.trim(), maxResults, temperature);
    }
  }

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <div className={styles.inputGroup}>
        <textarea
          id="query-input"
          className={styles.textarea}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query against the corporate document base..."
          rows={4}
          maxLength={4096}
          disabled={loading}
        />
        <div className={styles.inputFooter}>
          <button
            type="button"
            className={styles.paramsToggle}
            onClick={() => setShowParams(!showParams)}
          >
            {showParams ? "Hide parameters" : "Parameters"}
          </button>
          <span className={styles.charCount}>
            {query.length} / 4096
          </span>
        </div>
      </div>

      {showParams && (
        <div className={styles.params}>
          <div className={styles.param}>
            <label htmlFor="max-results" className={styles.paramLabel}>
              Max results
            </label>
            <input
              id="max-results"
              type="number"
              className={styles.paramInput}
              value={maxResults}
              onChange={(e) => setMaxResults(Number(e.target.value))}
              min={1}
              max={20}
            />
          </div>
          <div className={styles.param}>
            <label htmlFor="temperature" className={styles.paramLabel}>
              Temperature
            </label>
            <input
              id="temperature"
              type="number"
              className={styles.paramInput}
              value={temperature}
              onChange={(e) => setTemperature(Number(e.target.value))}
              min={0}
              max={2}
              step={0.1}
            />
          </div>
        </div>
      )}

      <Button
        type="submit"
        variant="primary"
        fullWidth
        loading={loading}
        disabled={!query.trim()}
      >
        Send Query
      </Button>
    </form>
  );
}
