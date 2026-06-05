"use client";

import { useTranslation } from "@/context/LanguageContext";
import styles from "./LanguageSwitcher.module.css";

export default function LanguageSwitcher() {
  const { locale, setLocale } = useTranslation();

  return (
    <div className={styles.switcher}>
      <button
        className={`${styles.btn} ${locale === "es" ? styles.active : ""}`}
        onClick={() => setLocale("es")}
      >
        ES
      </button>
      <div className={styles.divider} />
      <button
        className={`${styles.btn} ${locale === "en" ? styles.active : ""}`}
        onClick={() => setLocale("en")}
      >
        EN
      </button>
    </div>
  );
}
