from locust import HttpUser, task, between

class CornelioUser(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    def test_inference(self):
        """Test inference latency under load."""
        self.client.post("/api/v1/inference/generate", json={
            "prompt": "Summarize the primary benefits of using local inference models.",
            "max_tokens": 100,
            "temperature": 0.3
        })

    @task(2)
    def test_rag_query(self):
        """Test RAG query latency under load."""
        self.client.post("/api/v1/query", json={
            "query": "What are our corporate security policies?",
            "max_results": 3,
            "temperature": 0.1
        })

    @task(1)
    def test_health(self):
        """Test system readiness polling overhead."""
        self.client.get("/readiness")
