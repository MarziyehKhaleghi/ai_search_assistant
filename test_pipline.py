# test_pipeline.py

from services.document_loader import load_document
from services.chunker import chunk_text
from core.embeddings import embed_chunks
from services.vector_store import VectorStore
from services.ai_answer import answer_question
from core.config import DATA_PATH, CHUNK_SIZE, TOP_K

import os

def main():
    # 1 Finn dokumenter i DATA_PATH
    if not os.path.exists(DATA_PATH):
        print(f"ERROR: Data path {DATA_PATH} finnes ikke.")
        return

    file_list = [os.path.join(DATA_PATH, f) for f in os.listdir(DATA_PATH)
                 if f.lower().endswith((".txt", ".pdf", ".docx"))]

    if not file_list:
        print("Ingen dokumenter funnet i data-mappen. Legg til minst ett dokument.")
        return

    # Vi tester på første dokument for enkelhet
    file_path = file_list[0]
    print(f"\n=== Tester dokument: {file_path} ===")

    # 2 Last dokument
    try:
        text = load_document(file_path)
        print(f"Leste dokument med {len(text)} tegn.")
    except Exception as e:
        print(f"Feil under lasting av dokument: {e}")
        return

    # 3 Chunk dokumentet
    chunks = chunk_text(text, chunk_size=CHUNK_SIZE)
    print(f"Delte dokumentet i {len(chunks)} chunks.")

    # 4 Lag embeddings
    embedded_chunks = embed_chunks(chunks, source=file_path)
    print(f"Laget embeddings for {len(embedded_chunks)} chunks.")

    # 5 Opprett VectorStore og legg til chunks
    store = VectorStore()
    store.add(embedded_chunks)
    print("Vector store klar med alle chunks.")

    # 6 Still spørsmål
    query = "Hva handler dokumentet om?"
    result = answer_question(query, store, top_k=TOP_K)

    # 7 Skriv ut resultat
    print("\n=== RESULTAT ===")
    print("Spørsmål:", query)
    print("Svar:", result["answer"])
    print("\nTop-k kilder:")
    for src in result["sources"]:
        print(f"- ID {src['id']} | Score: {src['score']:.4f} | Metadata: {src['metadata']}")

if __name__ == "__main__":
    main()
