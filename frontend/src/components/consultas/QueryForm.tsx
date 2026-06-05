"use client";

import { useState } from "react";
import Button from "@/components/ui/Button";
import { useTranslation } from "@/context/LanguageContext";
import styles from "./QueryForm.module.css";

interface QueryFormProps {
  onSubmit: (query: string, maxResults: number, temperature: number) => void;
  loading: boolean;
}

export default function QueryForm({ onSubmit, loading }: QueryFormProps) {
  const { t } = useTranslation();
  const [query, setQuery] = useState("");
  const [maxResults, setMaxResults] = useState(3);
  const [temperature, setTemperature] = useState(0.1);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    onSubmit(query, maxResults, temperature);
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <div className={styles.field}>
        <textarea
          className={styles.textarea}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={t("consultas.query_placeholder")}
          rows={4}
          disabled={loading}
        />
      </div>

      <div className={styles.controls}>
        <div className={styles.controlGroup}>
          <label className={styles.label}>{t("consultas.max_results")} {maxResults}</label>
          <input
            type="range"
            min="1"
            max="10"
            value={maxResults}
            onChange={(e) => setMaxResults(Number(e.target.value))}
            disabled={loading}
          />
        </div>
        <div className={styles.controlGroup}>
          <label className={styles.label}>{t("consultas.temperature")} {temperature}</label>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={temperature}
            onChange={(e) => setTemperature(Number(e.target.value))}
            disabled={loading}
          />
        </div>
      </div>

      <div className={styles.actions}>
        <Button loading={loading} variant="primary">
          {loading ? t("consultas.processing") : t("consultas.submit")}
        </Button>
      </div>
    </form>
  );
}
