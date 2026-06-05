"use client";

import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import { useTranslation } from "@/context/LanguageContext";
import styles from "./TaskPanel.module.css";

export default function TaskPanel() {
  const { t } = useTranslation();

  return (
    <Card header={t("dashboard.tasks.title")}>
      <div className={styles.container}>
        <div className={styles.emptyState}>
          <p className={styles.emptyText}>{t("dashboard.tasks.empty")}</p>
        </div>
        <div className={styles.actions}>
          <Button variant="secondary">{t("dashboard.tasks.new_task")}</Button>
        </div>
      </div>
    </Card>
  );
}
