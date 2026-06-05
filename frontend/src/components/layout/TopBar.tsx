"use client";

import { useEffect, useState } from "react";
import StatusBadge from "@/components/ui/StatusBadge";
import LanguageSwitcher from "@/components/ui/LanguageSwitcher";
import { systemService } from "@/services/endpoints";
import { useTranslation } from "@/context/LanguageContext";
import styles from "./TopBar.module.css";

export default function TopBar() {
  const { t } = useTranslation();
  const [status, setStatus] = useState<"ready" | "degraded" | "offline" | "unknown">("unknown");

  useEffect(() => {
    let mounted = true;

    async function checkStatus() {
      try {
        const res = await systemService.readiness();
        if (mounted) setStatus(res.status as "ready" | "degraded" | "offline" | "unknown");
      } catch {
        if (mounted) setStatus("offline");
      }
    }

    checkStatus();
    const interval = setInterval(checkStatus, 30000);
    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  const getStatusText = () => {
    switch (status) {
      case "ready": return t("topbar.status_ready");
      case "degraded": return t("topbar.status_degraded");
      case "offline": return t("topbar.status_offline");
      default: return t("topbar.status_unknown");
    }
  };

  const getBadgeStatus = () => {
    switch (status) {
      case "ready": return "online";
      case "degraded": return "degraded";
      case "unknown": return "pending";
      default: return "offline";
    }
  };

  return (
    <header className={styles.topbar}>
      <div className={styles.left}>
        <div className={styles.breadcrumb}>
          <span className={styles.path}>CorpNet</span>
          <span className={styles.separator}>/</span>
          <span className={styles.current}>Cornelio Node</span>
        </div>
      </div>
      
      <div className={styles.right}>
        <LanguageSwitcher />
        <div className={styles.statusGroup}>
          <span className={styles.statusLabel}>System Status</span>
          <StatusBadge status={getBadgeStatus()} label={getStatusText()} />
        </div>
      </div>
    </header>
  );
}
