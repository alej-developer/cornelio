"use client";

import { useState } from "react";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import { useApi } from "@/hooks/useApi";
import { useNotification } from "@/context/NotificationContext";
import { reportService } from "@/services/endpoints";
import type { ReportResponse } from "@/types";
import styles from "./ReportPanel.module.css";

export default function ReportPanel() {
  const report = useApi<ReportResponse>();
  const { notify } = useNotification();
  const [expanded, setExpanded] = useState<string | null>(null);

  async function handleGenerate() {
    const result = await report.execute(() => reportService.generate());
    if (result) {
      notify("success", "Report generated successfully.");
    } else if (report.error) {
      notify("error", report.error);
    }
  }

  return (
    <Card header="Report Generation">
      <div className={styles.controls}>
        <p className={styles.description}>
          Generate an automated executive report from all indexed corporate documents.
        </p>
        <Button
          onClick={handleGenerate}
          loading={report.loading}
          variant="primary"
          size="md"
        >
          Generate Report
        </Button>
      </div>

      {report.error && !report.data && (
        <div className={styles.errorBanner}>{report.error}</div>
      )}

      {report.data && (
        <div className={styles.report}>
          <div className={styles.reportHeader}>
            <h3 className={styles.reportTitle}>{report.data.title}</h3>
            <span className={styles.reportMeta}>
              {report.data.document_count} documents | Generated{" "}
              {new Date(report.data.generated_at).toLocaleString()}
            </span>
          </div>

          <p className={styles.summary}>{report.data.summary}</p>

          <div className={styles.sections}>
            {report.data.sections.map((section, i) => (
              <div key={i} className={styles.section}>
                <button
                  className={styles.sectionHeader}
                  onClick={() =>
                    setExpanded(expanded === section.heading ? null : section.heading)
                  }
                >
                  <span>{section.heading}</span>
                  <span className={styles.chevron}>
                    {expanded === section.heading ? "\u2212" : "+"}
                  </span>
                </button>
                {expanded === section.heading && (
                  <div className={styles.sectionBody}>
                    <pre className={styles.sectionText}>{section.body}</pre>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </Card>
  );
}
