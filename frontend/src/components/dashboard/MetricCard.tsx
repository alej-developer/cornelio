import styles from "./MetricCard.module.css";

interface MetricCardProps {
  label: string;
  value: string | number;
  subtitle?: string;
  status?: "positive" | "neutral" | "negative";
}

export default function MetricCard({
  label,
  value,
  subtitle,
  status = "neutral",
}: MetricCardProps) {
  return (
    <div className={styles.card}>
      <span className={styles.label}>{label}</span>
      <span className={`${styles.value} ${styles[status]}`}>{value}</span>
      {subtitle && <span className={styles.subtitle}>{subtitle}</span>}
    </div>
  );
}
