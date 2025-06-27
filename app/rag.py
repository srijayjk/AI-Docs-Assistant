import numpy as np
from app.llm import generate_answer
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

    def has_documents(self):
        return self.collection.count() > 0

class RAGEngine:
    def __init__(self):
        self.index = ChromaVectorStore()
        if self.index.has_documents():
            print("✅ Existing vectors loaded from disk.")
        else:
            print("⚠️ No documents found. Please upload.")

    def build_index(self, docs):
        text_chunks = []
        metadatas = []
        for filename, text in docs:
            chunks = self.chunk_text(text)
            text_chunks.extend(chunks)
            metadatas.extend([{"source": filename}] * len(chunks))
        self.index.add(text_chunks, metadatas=metadatas)
        print("\n")
        print(f"📄 Processing {len(docs)} documents")
        print(f"✅ Added {len(text_chunks)} chunks to Chroma")

    def chunk_text(self, text, max_tokens=300):
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        return [chunk.page_content for chunk in splitter.create_documents([text])]

    def retrieve_context(self, question: str) -> str:
        print("\n")
        print(f"📄 Retreving context from documents ...")
        chunks = self.index.query(question, k=5)
        if chunks:
            context = "\n".join(chunks)
        else:
            context = "No context found in the document, Provide a generalized answer and inform there is no mathching content"
        return context

    def query(self, question, model="llama3.2:3b"):
        context = self.retrieve_context(question)
        full_prompt = f"Based on the following context, answer the question accurately and concisely. If the answer is not in the context, state that you don't know.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"

        try:
            generated_answer = generate_answer(
                full_prompt=full_prompt,
                model=model,
            )
            return generated_answer
        except Exception as e:
            print(f"⚠️ An unexpected error occurred during LLM generation: {e}")
            return "An internal error occurred during text generation."