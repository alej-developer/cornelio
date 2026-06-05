"use client";

import Sidebar from "./Sidebar";
import TopBar from "./TopBar";
import { NotificationProvider } from "@/context/NotificationContext";
import styles from "./MainLayout.module.css";
import type { ReactNode } from "react";

export default function MainLayout({ children }: { children: ReactNode }) {
  return (
    <NotificationProvider>
      <div className={styles.layout}>
        <Sidebar />
        <TopBar />
        <main className={styles.content}>{children}</main>
      </div>
    </NotificationProvider>
  );
}
