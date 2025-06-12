# DevBuddy-TinyLlama

🗓️ Project Timeline (8 Weeks)
✅ Week 1–2: Planning + Retrieval Pipeline
Choose a base model (e.g., Mistral-7B, TinyLlama, or Zephyr)

Set up basic RAG pipeline:

Ingest PDF/Markdown/code/docs

Use FAISS for embedding & similarity search

Wrap in a FastAPI server

✅ Week 3–4: Fine-Tuning
Use a sample Q&A dataset (e.g., StackOverflow, or synthesize from your docs)

Apply LoRA-based fine-tuning (Hugging Face PEFT)

Evaluate performance using a test set + qualitative tests

✅ Week 5–6: Infra + Observability
Containerize your service (Docker, FastAPI)

Add logging, rate limiting, basic auth

Add observability: latency tracking, request logging, error rates

Use Prometheus + Grafana or basic logging + Weights & Biases

✅ Week 7: Deployment
Deploy to GPU-backed infra (e.g., AWS ECS/GPU, Vertex AI, or GCP Cloud Run)

Set up autoscaling, load testing (Locust or k6)

✅ Week 8: Polish & Share
Write a blog post or README (how it works, tech stack, lessons)

Optional: Build a Streamlit/Next.js frontend for demo

🎯 Resume Angle
“Built a self-hosted LLM assistant with fine-tuned domain knowledge using LoRA; deployed on GPU-backed infra with full observability stack. Integrated RAG pipeline for real-time document search and response.”
