✅ Tech Stack
LLM: Open-source like Mistral 7B or LLama 3

RAG (Retrieval Augmented Generation): Use [LangChain] or [LlamaIndex]

OCR: [Tesseract OCR] for image-based PDFs

Document Parsing: pdfminer, PyMuPDF, or Unstructured.io

Vector DB: FAISS (local) or Chroma

Interface: CLI or Streamlit

Containerization: Docker



     [PDF/Image]        <-- User upload
          |
        /upload         <-- FastAPI
          |
        OCR/Text        <-- Extract content from file
          |
   +-----------------+
   | Chunk & Embed   |  <-- Text is split into chunks
   | via Sentence-    |
   | Transformers     |
   +-----------------+
          |
     Store in ChromaDB <-- Persistent vector DB
          |
        /ask           <-- User query
          |
   Query ChromaDB      <-- Retrieve top relevant chunks
          |
      Prompt LLM       <-- With context + question
          |
   Return Answer       <-- Via FastAPI
