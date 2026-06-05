"use client";

import Card from "@/components/ui/Card";
import QueryForm from "@/components/consultas/QueryForm";
import ResponseViewer from "@/components/consultas/ResponseViewer";
import DocumentUpload from "@/components/consultas/DocumentUpload";
import { useApi } from "@/hooks/useApi";
import { useNotification } from "@/context/NotificationContext";
import { queryService } from "@/services/endpoints";
import type { QueryResponse } from "@/types";
import styles from "./page.module.css";

export default function ConsultasPage() {
  const query = useApi<QueryResponse>();
  const { notify } = useNotification();

  async function handleQuery(
    queryText: string,
    maxResults: number,
    temperature: number,
  ) {
    const result = await query.execute(() =>
      queryService.query({
        query: queryText,
        max_results: maxResults,
        temperature,
        max_tokens: 512,
      }),
    );

    if (result) {
      notify("success", `Query processed in ${result.latency_ms.toFixed(0)}ms.`);
    } else if (query.error) {
      notify("error", query.error);
    }
  }

  return (
    <div className={styles.consultas}>
      <div className={styles.left}>
        <Card header="RAG Query">
          <QueryForm onSubmit={handleQuery} loading={query.loading} />
        </Card>

        <Card header="Document Upload">
          <DocumentUpload />
        </Card>
      </div>

      <div className={styles.right}>
        <Card header="Response">
          <ResponseViewer
            response={query.data}
            loading={query.loading}
            error={query.error}
          />
        </Card>
      </div>
    </div>
  );
}
