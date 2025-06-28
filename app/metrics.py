from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter("llm_requests_total", "Total number of LLM requests")
REQUEST_FAILURES = Counter("llm_request_failures", "Number of failed LLM requests")
REQUEST_LATENCY = Histogram("llm_request_latency_seconds", "Latency of LLM requests")
