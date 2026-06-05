"use client";

import Card from "@/components/ui/Card";
import QueryForm from "@/components/consultas/QueryForm";
import ResponseViewer from "@/components/consultas/ResponseViewer";
import DocumentUpload from "@/components/consultas/DocumentUpload";
import { useApi } from "@/hooks/useApi";
import { useNotification } from "@/context/NotificationContext";
import { useTranslation } from "@/context/LanguageContext";
import { queryService } from "@/services/endpoints";
import type { QueryResponse } from "@/types";
import styles from "./page.module.css";

export default function ConsultasPage() {
  const query = useApi<QueryResponse>();
  const { notify } = useNotification();
  const { t } = useTranslation();

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
        <Card header={t("consultas.rag_query")}>
          <QueryForm onSubmit={handleQuery} loading={query.loading} />
        </Card>

        <Card header={t("consultas.document_upload")}>
          <DocumentUpload />
        </Card>
      </div>

      <div className={styles.right}>
        <Card header={t("consultas.response")}>
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
