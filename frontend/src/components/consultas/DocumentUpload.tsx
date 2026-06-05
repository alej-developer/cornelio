"use client";

import { useRef, useState } from "react";
import Button from "@/components/ui/Button";
import { useApi } from "@/hooks/useApi";
import { useNotification } from "@/context/NotificationContext";
import { documentService } from "@/services/endpoints";
import type { DocumentUploadResponse } from "@/types";
import styles from "./DocumentUpload.module.css";

const ACCEPTED_TYPES = ["application/pdf", "text/plain"];
const MAX_SIZE_MB = 50;

export default function DocumentUpload() {
  const upload = useApi<DocumentUploadResponse>();
  const { notify } = useNotification();
  const fileRef = useRef<HTMLInputElement>(null);
  const [dragOver, setDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  function validateFile(file: File): string | null {
    if (!ACCEPTED_TYPES.includes(file.type)) {
      return "Unsupported format. Accepted: PDF, TXT.";
    }
    if (file.size > MAX_SIZE_MB * 1024 * 1024) {
      return `File exceeds ${MAX_SIZE_MB} MB limit.`;
    }
    return null;
  }

  function handleFileSelect(file: File) {
    const error = validateFile(file);
    if (error) {
      notify("error", error);
      return;
    }
    setSelectedFile(file);
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFileSelect(file);
  }

  function handleInputChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file) handleFileSelect(file);
  }

  async function handleUpload() {
    if (!selectedFile) return;

    const result = await upload.execute(() =>
      documentService.upload(selectedFile),
    );

    if (result) {
      notify(
        "success",
        `"${result.filename}" indexed: ${result.chunks_created} chunks created.`,
      );
      setSelectedFile(null);
      if (fileRef.current) fileRef.current.value = "";
    } else if (upload.error) {
      notify("error", upload.error);
    }
  }

  return (
    <div className={styles.wrapper}>
      <div
        className={`${styles.dropzone} ${dragOver ? styles.dragOver : ""}`}
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        onClick={() => fileRef.current?.click()}
      >
        <input
          ref={fileRef}
          type="file"
          className={styles.fileInput}
          accept=".pdf,.txt,application/pdf,text/plain"
          onChange={handleInputChange}
        />

        <svg width="28" height="28" viewBox="0 0 28 28" fill="none" stroke="var(--text-muted)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <path d="M14 18V6" />
          <path d="M9 11l5-5 5 5" />
          <path d="M3 18v4a2 2 0 002 2h18a2 2 0 002-2v-4" />
        </svg>

        <p className={styles.dropText}>
          {selectedFile
            ? selectedFile.name
            : "Drop a file here or click to browse"}
        </p>
        <span className={styles.dropHint}>PDF or TXT, up to {MAX_SIZE_MB} MB</span>
      </div>

      {selectedFile && (
        <Button
          onClick={handleUpload}
          loading={upload.loading}
          variant="primary"
          fullWidth
        >
          Upload and Index
        </Button>
      )}

      {upload.error && !upload.data && (
        <div className={styles.errorBanner}>{upload.error}</div>
      )}
    </div>
  );
}
