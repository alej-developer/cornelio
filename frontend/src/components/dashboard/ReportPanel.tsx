"use client";

import { useState } from "react";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import { useTranslation } from "@/context/LanguageContext";
import styles from "./ReportPanel.module.css";

export default function ReportPanel() {
  const { t } = useTranslation();
  const [loading, setLoading] = useState(false);
  const [reportUrl, setReportUrl] = useState<string | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    // Simulate API call for report generation
    setTimeout(() => {
      setLoading(false);
      setReportUrl("#");
    }, 2000);
  };

  return (
    <Card header={t("dashboard.reports.title")}>
      <div className={styles.container}>
        <Button onClick={handleGenerate} loading={loading} variant="primary">
          {loading ? t("dashboard.reports.generating") : t("dashboard.reports.generate_btn")}
        </Button>

        {reportUrl && (
          <div className={styles.result}>
            <a href={reportUrl} className={styles.downloadLink}>
              Download Report.pdf
            </a>
          </div>
        )}
      </div>
    </Card>
  );
}
