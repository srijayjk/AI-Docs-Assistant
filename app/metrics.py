from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter("llm_requests_total", "Total number of LLM requests")
REQUEST_FAILURES = Counter("llm_request_failures", "Number of failed LLM requests")
REQUEST_LATENCY = Histogram("llm_request_latency_seconds", "Latency of LLM requests")


# Token count metrics
INPUT_TOKENS = Histogram(
    "llm_input_tokens",
    "Number of input tokens per request",
    buckets=[10, 50, 100, 200, 400, 600, 800, 1000]
)

OUTPUT_TOKENS = Histogram(
    "llm_output_tokens",
    "Number of output tokens per request",
    buckets=[10, 50, 100, 200, 400, 600]
)

# Similarity score (cosine similarity)
SIMILARITY_SCORE = Histogram(
    "rag_similarity_score",
    "Cosine similarity score of top retrieved document",
    buckets=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
)