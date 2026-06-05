"use client";

import { useEffect, useState } from "react";
import MetricCard from "@/components/dashboard/MetricCard";
import TaskPanel from "@/components/dashboard/TaskPanel";
import ReportPanel from "@/components/dashboard/ReportPanel";
import { systemService } from "@/services/endpoints";
import type { ReadinessResponse } from "@/types";
import styles from "./page.module.css";

export default function DashboardPage() {
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

  const mlxStatus = readiness?.mlx_model_loaded ? "Loaded" : "Not loaded";
  const vectorStatus = readiness?.vector_store_ready ? "Ready" : "Offline";

  return (
    <div className={styles.dashboard}>
      <section className={styles.metrics}>
        <MetricCard
          label="MLX Model"
          value={mlxStatus}
          status={readiness?.mlx_model_loaded ? "positive" : "neutral"}
          subtitle="Local inference engine"
        />
        <MetricCard
          label="Vector Store"
          value={vectorStatus}
          status={readiness?.vector_store_ready ? "positive" : "neutral"}
          subtitle="ChromaDB document index"
        />
        <MetricCard
          label="API Status"
          value={readiness ? "Online" : "Checking"}
          status={readiness ? "positive" : "neutral"}
          subtitle="FastAPI backend"
        />
        <MetricCard
          label="System"
          value={readiness?.status || "Unknown"}
          status={
            readiness?.status === "ready"
              ? "positive"
              : readiness?.status === "degraded"
                ? "neutral"
                : "negative"
          }
          subtitle="Overall health"
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
