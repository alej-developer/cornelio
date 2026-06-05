import styles from "./Card.module.css";
import type { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  header?: ReactNode;
  className?: string;
  noPadding?: boolean;
}

export default function Card({ children, header, className, noPadding }: CardProps) {
  return (
    <div className={`${styles.card} ${className || ""}`}>
      {header && <div className={styles.header}>{header}</div>}
      <div className={noPadding ? styles.bodyNoPad : styles.body}>
        {children}
      </div>
    </div>
  );
}
