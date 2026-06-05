"use client";

import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import StatusBadge from "@/components/ui/StatusBadge";
import { systemService } from "@/services/endpoints";
import styles from "./TopBar.module.css";

const ROUTE_TITLES: Record<string, string> = {
  "/dashboard": "Dashboard",
  "/consultas": "Consultas",
};

export default function TopBar() {
  const pathname = usePathname();
  const [systemStatus, setSystemStatus] = useState<"online" | "offline" | "degraded">("pending" as "online" | "offline" | "degraded");

  const title = ROUTE_TITLES[pathname] || "Cornelio";

  useEffect(() => {
    let mounted = true;

    async function checkSystem() {
      try {
        const data = await systemService.readiness();
        if (!mounted) return;
        if (data.mlx_model_loaded && data.vector_store_ready) {
          setSystemStatus("online");
        } else {
          setSystemStatus("degraded");
        }
      } catch {
        if (mounted) setSystemStatus("offline");
      }
    }

    checkSystem();
    const interval = setInterval(checkSystem, 30_000);

    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  return (
    <header className={styles.topbar}>
      <div className={styles.left}>
        <h1 className={styles.title}>{title}</h1>
      </div>
      <div className={styles.right}>
        <StatusBadge status={systemStatus} label={`System: ${systemStatus}`} />
      </div>
    </header>
  );
}
