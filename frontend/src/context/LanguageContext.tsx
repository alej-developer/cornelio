"use client";

import React, { createContext, useContext, useState, ReactNode } from "react";
import es from "@/locales/es.json";
import en from "@/locales/en.json";

type Locale = "es" | "en";
type Dictionary = typeof es;

const dictionaries: Record<Locale, Dictionary> = {
  es,
  en,
};

interface LanguageContextProps {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  t: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextProps | undefined>(
  undefined,
);

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [locale, setLocale] = useState<Locale>("es");

  const t = (keyPath: string): string => {
    const keys = keyPath.split(".");
    let current: any = dictionaries[locale];

    for (const key of keys) {
      if (current[key] === undefined) {
        console.warn(`Missing translation key: ${keyPath}`);
        return keyPath;
      }
      current = current[key];
    }

    return current as string;
  };

  return (
    <LanguageContext.Provider value={{ locale, setLocale, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useTranslation() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error("useTranslation must be used within a LanguageProvider");
  }
  return context;
}
