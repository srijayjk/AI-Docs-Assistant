import numpy as np
from app.llm import generate_answer
import uuid

import chromadb
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter
from prometheus_client import Summary
from app.metrics import REQUEST_COUNT, REQUEST_FAILURES, REQUEST_LATENCY, INPUT_TOKENS, OUTPUT_TOKENS, SIMILARITY_SCORE
import time


def count_tokens(text: str) -> int:
    return len(text.split())

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

    def query(self, question, model="llama3.2:3b"):
        start = time.time()
        REQUEST_COUNT.inc()

        try:
            # Retrieve context from top-k similar documents
            print("\n📄 Retreving context from documents ...")
            chunks = self.index.collection.query(query_texts=[question], n_results=1)
            # Log similarity score if available
            if chunks and "distances" in chunks and chunks["distances"][0]:
                similarity = 1 - chunks["distances"][0][0]  # cosine similarity
                SIMILARITY_SCORE.observe(similarity)

            if chunks and "documents" in chunks and chunks["documents"][0]:
                context = "\n".join(chunks["documents"][0])
            else:
                context = "No context found in the document. Provide a general answer and mention missing content."

            full_prompt = f"""You are a helpfull and polite assistant. Answer the question accurately and concisely. 
                Context:
                {context}
                Question: {question}

                Answer:"""

            # Log input tokens
            input_tokens = count_tokens(full_prompt)
            INPUT_TOKENS.observe(input_tokens)

            generated_answer = generate_answer(full_prompt=full_prompt, model=model)

            # Log output tokens
            output_tokens = count_tokens(generated_answer)
            OUTPUT_TOKENS.observe(output_tokens)

            print(f"📤 Full prompt:\n{full_prompt}")
            print(f"📥 LLM output:\n{generated_answer}")

            return generated_answer

        except Exception as e:
            REQUEST_FAILURES.inc()
            print(f"⚠️ An unexpected error occurred during LLM generation: {e}")
            return "An internal error occurred during text generation."

        finally:
            REQUEST_LATENCY.observe(time.time() - start)