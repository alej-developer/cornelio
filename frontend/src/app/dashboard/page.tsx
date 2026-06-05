"use client";

import { useEffect, useState } from "react";
import MetricCard from "@/components/dashboard/MetricCard";
import TaskPanel from "@/components/dashboard/TaskPanel";
import ReportPanel from "@/components/dashboard/ReportPanel";
import { systemService } from "@/services/endpoints";
import { useTranslation } from "@/context/LanguageContext";
import type { ReadinessResponse } from "@/types";
import styles from "./page.module.css";

export default function DashboardPage() {
  const { t } = useTranslation();
  const [readiness, setReadiness] = useState<ReadinessResponse | null>(null);

  useEffect(() => {
    let mounted = true;

    async function fetch() {
      try {
        const data = await systemService.readiness();
        if (mounted) setReadiness(data);
      } catch {
        /* system unavailable — metrics will show defaults */
      }
    }

    fetch();
    return () => { mounted = false; };
  }, []);

  const mlxStatus = readiness?.mlx_model_loaded ? t("dashboard.mlx_loaded") : t("dashboard.mlx_not_loaded");
  const vectorStatus = readiness?.vector_store_ready ? t("dashboard.vector_ready") : t("dashboard.vector_offline");

  return (
    <div className={styles.dashboard}>
      <section className={styles.metrics}>
        <MetricCard
          label={t("dashboard.mlx_model")}
          value={mlxStatus}
          status={readiness?.mlx_model_loaded ? "positive" : "neutral"}
          subtitle={t("dashboard.mlx_subtitle")}
        />
        <MetricCard
          label={t("dashboard.vector_store")}
          value={vectorStatus}
          status={readiness?.vector_store_ready ? "positive" : "neutral"}
          subtitle={t("dashboard.vector_subtitle")}
        />
        <MetricCard
          label={t("dashboard.api_status")}
          value={readiness ? t("dashboard.api_online") : t("dashboard.api_checking")}
          status={readiness ? "positive" : "neutral"}
          subtitle={t("dashboard.api_subtitle")}
        />
        <MetricCard
          label={t("dashboard.system")}
          value={readiness?.status || t("topbar.status_unknown")}
          status={
            readiness?.status === "ready"
              ? "positive"
              : readiness?.status === "degraded"
                ? "neutral"
                : "negative"
          }
          subtitle={t("dashboard.system_subtitle")}
        />
      </section>

      <section className={styles.panels}>
        <div className={styles.panelLeft}>
          <TaskPanel />
        </div>
        <div className={styles.panelRight}>
          <ReportPanel />
        </div>
      </section>
    </div>
  );
}
