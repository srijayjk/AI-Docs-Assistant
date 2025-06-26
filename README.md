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
