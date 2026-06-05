"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTranslation } from "@/context/LanguageContext";
import styles from "./Sidebar.module.css";

interface NavItem {
  href: string;
  label: string;
  icon: React.ReactNode;
}

const DashboardIcon = (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="2" width="6" height="6" rx="1" />
    <rect x="10" y="2" width="6" height="6" rx="1" />
    <rect x="2" y="10" width="6" height="6" rx="1" />
    <rect x="10" y="10" width="6" height="6" rx="1" />
  </svg>
);

const ConsultasIcon = (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="8" cy="8" r="5.5" />
    <line x1="12" y1="12" x2="16" y2="16" />
  </svg>
);

export default function Sidebar() {
  const pathname = usePathname();
  const { t } = useTranslation();

  const NAV_ITEMS: NavItem[] = [
    { href: "/dashboard", label: t("sidebar.dashboard"), icon: DashboardIcon },
    { href: "/consultas", label: t("sidebar.consultas"), icon: ConsultasIcon },
  ];

  return (
    <aside className={styles.sidebar}>
      <div className={styles.brand}>
        <div className={styles.logoMark}>C</div>
        <div className={styles.brandText}>
          <span className={styles.brandName}>Cornelio</span>
          <span className={styles.brandTag}>MLX Platform</span>
        </div>
      </div>

      <nav className={styles.nav}>
        <span className={styles.navLabel}>Navigation</span>
        {NAV_ITEMS.map((item) => {
          const isActive =
            pathname === item.href || pathname.startsWith(item.href + "/");
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`${styles.navItem} ${isActive ? styles.active : ""}`}
            >
              <span className={styles.navIcon}>{item.icon}</span>
              <span>{item.label}</span>
              {isActive && <span className={styles.activeBar} />}
            </Link>
          );
        })}
      </nav>

      <div className={styles.footer}>
        <div className={styles.footerDivider} />
        <div className={styles.footerContent}>
          <span className={styles.version}>v0.1.0</span>
          <span className={styles.engine}>Apple MLX</span>
        </div>
      </div>
    </aside>
  );
}
