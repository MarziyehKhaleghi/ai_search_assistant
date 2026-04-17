from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import os
from pydantic import BaseModel
from services.vector_store import VectorStore
from services.document_loader import load_document
from services.chunker import chunk_text
from core.embeddings import embed_chunks
from services.ai_answer import answer_question
from core.config import DATA_PATH, CHUNK_SIZE, TOP_K


app = FastAPI(
    title="AI Search Assistant",
    version="0.1.0",
)

# Tillat React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_store = VectorStore()
print("✅ VectorStore er opprettet og klar.")

def load_documents_once():
    """
    Leser alle dokumenter i DATA_PATH.
    Lager embeddings kun for nye dokumenter.
    """
    if not os.path.exists(DATA_PATH):
        print(f"❌ Data path finnes ikke: {DATA_PATH}")
        return

    for filename in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, filename)

        # hopp over mapper
        if not os.path.isfile(file_path):
            continue

        # støttede filtyper
        if not filename.lower().endswith((".txt", ".pdf", ".docx")):
            continue

        # sjekk om dokumentet allerede er embedded
        already_indexed = any(
            chunk["metadata"]["source"] == file_path
            for chunk in vector_store.data.values()
        )

        if already_indexed:
            print(f"⏭️  Hopper over eksisterende dokument: {filename}")
            continue

        print(f"📄 Leser nytt dokument: {filename}")

        # last, chunk, embed
        text = load_document(file_path)
        chunks = chunk_text(text, CHUNK_SIZE)
        embedded_chunks = embed_chunks(chunks, source=file_path)

        # legg i vector store (og lagre)
        vector_store.add(embedded_chunks)

        print(f"✅ Dokument indeksert: {filename}")


@app.on_event("startup")
def startup_event():
    print("🚀 Starter FastAPI – laster dokumenter én gang")
    load_documents_once()

class QueryRequest(BaseModel):
    query:str

@app.post("/search")
def search_endpoint(request: QueryRequest):
    answer = answer_question(request.query, vector_store, top_k = TOP_K)
    return answer
    



@app.get("/health")
def health_check():
    return {"status": "ok"}
