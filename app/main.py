from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from app.ingest import load_text_from_pdf, load_text_from_image
from app.rag import RAGEngine
from app.auth import verify_api_key
from pydantic import BaseModel
import os
import shutil

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
        raise HTTPException(status_code=400, detail="Unsupported file type")

    rag.build_index([(file.filename, text)])
    return {"message": "Document uploaded and indexed successfully"}

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(
    request: QueryRequest,
    api_key: str = Depends(verify_api_key)
):
    # rag.query should return answer, confidence, sources tuple for UI integration
    result = rag.query(request.question, model="llama3.2:3b")

    # If your rag.query currently returns just the answer string,
    # adapt here accordingly:
    if isinstance(result, str):
        answer = result
        confidence = None
        sources = []
    else:
        # Expected tuple: (answer, confidence, sources)
        answer, confidence, sources = result

    return {
        "answer": answer,
        "confidence": confidence,
        "sources": sources
    }
