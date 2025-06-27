from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from app.ingest import load_text_from_pdf, load_text_from_image
from app.rag import RAGEngine
from app.auth import verify_api_key
from pydantic import BaseModel
import os
import shutil
import requests


app = FastAPI()
rag = RAGEngine()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)

UPLOAD_DIR = "data/docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"status": "running"}

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    ext = file.filename.lower().split(".")[-1]
    if ext == "pdf":
        text = load_text_from_pdf(file_path)
    elif ext in ("png", "jpg", "jpeg", "tiff"):
        text = load_text_from_image(file_path)
    else:
        # Clean up the unsupported file
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Unsupported file type")

    rag.build_index([(file.filename, text)])
    return {"message": "Document uploaded and indexed successfully", "filename": file.filename}

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(
    request: QueryRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Asks a question to the RAG engine, which uses the indexed documents and Llama 3.2.
    """
    print(f"Received question: {request.question}")
    # The rag.query method now handles the context retrieval and LLM call
    # We pass the desired Ollama model name
    try:
        result = rag.query(request.question, model="llama3.2:3b")
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {e}")


class PromptRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat(req: PromptRequest):
    response = requests.post(
        "http://ollama:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": req.prompt,
            "stream": False
        }
    )
    return response.json()