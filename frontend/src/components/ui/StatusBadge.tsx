import styles from "./StatusBadge.module.css";

interface StatusBadgeProps {
  status: "online" | "offline" | "degraded" | "pending";
  label?: string;
}

const STATUS_LABELS: Record<StatusBadgeProps["status"], string> = {
  online: "Online",
  offline: "Offline",
  degraded: "Degraded",
  pending: "Pending",
};

export default function StatusBadge({ status, label }: StatusBadgeProps) {
  return (
    <span className={`${styles.badge} ${styles[status]}`}>
      <span className={styles.dot} />
      {label || STATUS_LABELS[status]}
    </span>
  );
}
