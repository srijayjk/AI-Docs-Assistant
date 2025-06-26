import numpy as np
from app.llm import generate_answer
from sentence_transformers import SentenceTransformer
import uuid

import chromadb
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter


class ChromaVectorStore:
    def __init__(self, persist_directory="chroma_store"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = self.client.get_or_create_collection(
            name="rag_store", embedding_function=self.embedding_fn
        )

    def add(self, texts, metadatas=None, ids=None):
        if not ids:
            ids = [str(uuid.uuid4()) for _ in range(len(texts))]
            # ids = [f"doc_{i}" for i in range(len(texts))]
        if not metadatas:
            metadatas = [{}] * len(texts)
        self.collection.add(documents=texts, metadatas=metadatas, ids=ids)

    def query(self, text, k=2):
        results = self.collection.query(query_texts=[text], n_results=k)
        return results["documents"][0]


class RAGEngine:
    def __init__(self):
        self.index = ChromaVectorStore()
    
    def build_index(self, docs):
        text_chunks = []
        metadatas = []
        for filename, text in docs:
            chunks = self.chunk_text(text)
            text_chunks.extend(chunks)
            metadatas.extend([{"source": filename}] * len(chunks))
        self.index.add(text_chunks, metadatas=metadatas)
        print(f"📄 Processing {len(docs)} documents")
        print(f"✅ Added {len(text_chunks)} chunks to Chroma")

    def chunk_text(self, text, max_tokens=300):
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        return [chunk.page_content for chunk in splitter.create_documents([text])]

    def query(self, question, model="mistral"):
        chunks = self.index.query(question, k=5)
        print("🔎 Query result:")
        print(self.index.query("What is the purpose of the manual?", k=5))
        context = "\n".join(chunks)
        return generate_answer(question, context, model=model)