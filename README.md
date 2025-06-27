
# 🧠 AI Docs Assistant

An AI-powered document question-answering application built using FastAPI, Streamlit, ChromaDB, and LLMs (LLaMA3 via Ollama). Upload PDFs/images and ask natural language questions about the content.

---

## 🚀 Features

- 📄 Upload documents (PDFs/images)
- 🤖 Ask questions in natural language
- 🧠 Uses RAG (Retrieval-Augmented Generation)
- 💾 Vector store with ChromaDB
- 🧰 GPU-enabled embeddings via SentenceTransformer
- 🔐 API key-protected endpoints
- 📊 Streamlit UI with file list, history, and confidence scores
- 📦 Dockerized backend for easy deployment

---
     [PDF/Image]             <-- User upload
          |
        /upload              <-- FastAPI
          |
        OCR/Text             <-- Extract content from file
          |
    Chunk & Embed            <-- Text is split into chunks
    via Sentence-    
    Transformers     
          |
     Store in ChromaDB       <-- Persistent vector DB
          |
        ask                  <-- User query
          |
     Query ChromaDB          <-- Retrieve top relevant chunks
          |
      Prompt LLM             <-- With context + question
          |
     Return Answer           <-- Via FastAPI
---

## 📂 Project Structure
```bash
AI-Docs-Assistant/
├── app/
│ ├── main.py # FastAPI app
│ ├── auth.py # API key verification
│ ├── ingest.py # PDF/image text extraction
│ ├── rag.py # RAG engine & Chroma vector store
├── ui/
│ └── streamlit_app.py # Frontend interface
├── data/docs/ # Uploaded documents
├── requirements.txt
├── Dockerfile
├── .env
└── README.md
```
---

## ⚙️ Prerequisites

- Python 3.10+
- Docker
- Ollama (for running local LLMs like LLaMA3)
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ollama run llama3
  ```

🧪 Setup Locally (Without Docker)
1. Clone the repo
```bash
git clone https://github.com/yourusername/AI-Docs-Assistant.git
cd AI-Docs-Assistant
```
2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Run FastAPI backend
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
5. Run Streamlit frontend
```bash
streamlit run ui/streamlit_app.py
```


## 🔐 API Authentication
Add your key in .env:

API_KEY=srijaykey123
-H "X-API-Key: srijaykey123"


## 📦 Docker Deployment
1. Build the Docker image
```bash
docker compose up --build
```
2. Run the container
```bash
docker-compose up
```
(Optional) Use Docker Compose (if docker-compose.yml is added)

🧠 Example Usage
3. Upload a Document
```bash
curl -X POST http://localhost:8000/upload \
  -H "X-API-Key: srijaykey123" \
  -F "file=@data/docs/sample.pdf"
```
4. Ask a Question
```bash
curl -X POST http://localhost:8000/ask \
  -H "X-API-Key: srijaykey123" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the document about?"}'
```

## 🛠 Tech Stack
- Backend: FastAPI
- Frontend: Streamlit
- Vector DB: Chroma
- Embeddings: RecursiveCharacterTextSplitter
- OCR/Parsing: unstructured, PyMuPDF, Tesseract
- LLM: LLaMA3 via Ollama


## 🧹 Cleanup / Reset
You can clear the vector store manually:
```bash
rm -rf chroma_store/
```
Or programmatically in your app.


## 📬 Contact
Made with ❤️ by Srijay Kolvekar

📄 License
MIT License

---
