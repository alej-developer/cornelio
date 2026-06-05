"use client";

/**
 * [ES] Contexto global de notificaciones con renderizado de toasts. / [EN] Global notification context with toast rendering.
 *
 * [ES] Las notificaciones se ocultan tras 5 segundos. / [EN] Notifications are hidden after 5 seconds.
 * [ES] Los estilos se definen en globals.css (clases notification-*). / [EN] Styles are defined in globals.css (notification-* classes).
 */

import {
  createContext,
  useCallback,
  useContext,
  useState,
  type ReactNode,
} from "react";
import type { Notification, NotificationType } from "@/types";

interface NotificationContextType {
  notifications: Notification[];
  notify: (type: NotificationType, message: string) => void;
  dismiss: (id: string) => void;
}

const NotificationContext = createContext<NotificationContextType | null>(null);

const AUTO_DISMISS_MS = 5000;

export function NotificationProvider({ children }: { children: ReactNode }) {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const notify = useCallback((type: NotificationType, message: string) => {
    const id = Date.now().toString(36) + Math.random().toString(36).slice(2);
    setNotifications((prev) => [...prev, { id, type, message }]);
    setTimeout(() => {
      setNotifications((prev) => prev.filter((n) => n.id !== id));
    }, AUTO_DISMISS_MS);
  }, []);

  const dismiss = useCallback((id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  }, []);

  return (
    <NotificationContext.Provider value={{ notifications, notify, dismiss }}>
      {children}
      {notifications.length > 0 && (
        <div className="notification-container" role="status" aria-live="polite">
          {notifications.map((n) => (
            <div
              key={n.id}
              className={`notification-toast notification-${n.type}`}
            >
              <span>{n.message}</span>
              <button
                onClick={() => dismiss(n.id)}
                className="notification-dismiss"
                aria-label="Dismiss notification"
              >
                &times;
              </button>
            </div>
          ))}
        </div>
      )}
    </NotificationContext.Provider>
  );
}

export function useNotification(): NotificationContextType {
  const ctx = useContext(NotificationContext);
  if (!ctx) {
    throw new Error("useNotification must be used within a NotificationProvider.");
  }
  return ctx;
}
