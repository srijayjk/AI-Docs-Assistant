✅ Tech Stack
LLM: Open-source LLama 3
RAG (Retrieval Augmented Generation)
OCR: Tesseract OCR for image-based PDFs
Document Parsing: pdfminer
Vector DB: Chroma
Interface: CLI or Streamlit
Containerization: Docker



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

## 📂 Project Structure


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




---

## ⚙️ Prerequisites

- Python 3.10+
- Docker
- Ollama (for running local LLMs like LLaMA3)
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ollama run llama3


🧪 Setup Locally (Without Docker)
1. Clone the repo
bash
Copy
Edit

git clone https://github.com/yourusername/AI-Docs-Assistant.git
cd AI-Docs-Assistant


2. Create and activate virtual environment
bash
Copy
Edit
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate


3. Install dependencies
bash
Copy
Edit

pip install -r requirements.txt


4. Run FastAPI backend
bash
Copy
Edit
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

5. Run Streamlit frontend
bash
Copy
Edit
streamlit run ui/streamlit_app.py



🔐 API Authentication
Add your key in .env:

API_KEY=srijaykey123

-H "X-API-Key: srijaykey123"


📦 Docker Deployment
1. Build the Docker image
bash
Copy
Edit
docker build -t ai-docs-assistant .
2. Run the container
bash
Copy
Edit
docker run -p 8000:8000 ai-docs-assistant
(Optional) Use Docker Compose (if docker-compose.yml is added)
🧠 Example Usage
Upload a Document
bash
Copy
Edit
curl -X POST http://localhost:8000/upload \
  -H "X-API-Key: srijaykey123" \
  -F "file=@data/docs/sample.pdf"
Ask a Question
bash
Copy
Edit
curl -X POST http://localhost:8000/ask \
  -H "X-API-Key: srijaykey123" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the document about?"}'
🛠 Tech Stack
Backend: FastAPI

Frontend: Streamlit

Vector DB: Chroma

Embeddings: sentence-transformers (all-MiniLM-L6-v2)

OCR/Parsing: unstructured, PyMuPDF, Tesseract

LLM: LLaMA3 via Ollama

🧠 AI Infrastructure Concepts Used
Vector databases (Chroma)

GPU-accelerated embedding generation

Retrieval-augmented generation (RAG)

Modular service-based architecture

Docker containerization

API key-based security

Logs & dev reload with watchfiles

🧹 Cleanup / Reset
You can clear the vector store manually:

bash
Copy
Edit
rm -rf chroma_store/
Or programmatically in your app.

📬 Contact
Made with ❤️ by Srijay Kolvekar

📄 License
MIT License

yaml
Copy
Edit

---

Let me know if you'd like to:
- Add images or demo GIFs
- Add deployment steps to cloud platforms (Render, Hugging Face, AWS)
- Include Docker Compose

Would you like help generating those?
