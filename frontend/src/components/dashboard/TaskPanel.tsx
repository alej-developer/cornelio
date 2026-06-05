"use client";

import Card from "@/components/ui/Card";
import styles from "./TaskPanel.module.css";
import type { AutomatedTask, TaskStatus } from "@/types";

const STATUS_MAP: Record<TaskStatus, { label: string; className: string }> = {
  completed: { label: "Completed", className: styles.completed },
  running: { label: "Running", className: styles.running },
  pending: { label: "Pending", className: styles.pending },
  failed: { label: "Failed", className: styles.failed },
};

const MOCK_TASKS: AutomatedTask[] = [
  {
    id: "t1",
    name: "Daily Document Sync",
    status: "completed",
    description: "Synchronize corporate documents from shared storage.",
    lastRun: "2026-06-05T10:00:00Z",
  },
  {
    id: "t2",
    name: "Vector Store Reindex",
    status: "running",
    description: "Rebuild vector embeddings for all indexed documents.",
    lastRun: "2026-06-05T14:30:00Z",
  },
  {
    id: "t3",
    name: "Weekly Summary Report",
    status: "pending",
    description: "Generate automated executive summary from knowledge base.",
    lastRun: null,
  },
  {
    id: "t4",
    name: "Model Health Check",
    status: "completed",
    description: "Validate MLX model integrity and response latency.",
    lastRun: "2026-06-05T12:00:00Z",
  },
];

function formatTime(iso: string | null): string {
  if (!iso) return "Never";
  try {
    const d = new Date(iso);
    return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  } catch {
    return "Unknown";
  }
}

export default function TaskPanel() {
  return (
    <Card header="Automated Tasks">
      <div className={styles.list}>
        {MOCK_TASKS.map((task) => {
          const statusInfo = STATUS_MAP[task.status];
          return (
            <div key={task.id} className={styles.row}>
              <div className={styles.info}>
                <span className={styles.taskName}>{task.name}</span>
                <span className={styles.taskDesc}>{task.description}</span>
              </div>
              <div className={styles.meta}>
                <span className={styles.time}>
                  Last: {formatTime(task.lastRun)}
                </span>
                <span className={`${styles.status} ${statusInfo.className}`}>
                  {statusInfo.label}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
}
