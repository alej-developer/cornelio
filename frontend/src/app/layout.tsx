import type { Metadata } from "next";
import MainLayout from "@/components/layout/MainLayout";
import "./globals.css";

export const metadata: Metadata = {
  title: "Cornelio — MLX Corporate Platform",
  description:
    "Corporate inference and document intelligence platform powered by Apple MLX. "
    + "Query documents, automate tasks, and generate reports through a secure, local-first interface.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <MainLayout>{children}</MainLayout>
      </body>
    </html>
  );
}
