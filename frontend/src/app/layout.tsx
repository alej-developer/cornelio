import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Cornelio — MLX Inference Platform",
  description:
    "Corporate inference interface powered by Apple MLX. Interact with locally-hosted language models through a secure, high-performance web client.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
