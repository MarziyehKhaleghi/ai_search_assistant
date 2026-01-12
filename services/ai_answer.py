from core.embeddings import create_embedding
from core.client import get_client
import numpy as np


def answer_question(query: str, vector_store, top_k: int = 5) -> dict:
    """
    Tar et spørsmål, søker i vector store og genererer et AI-svar.
    """
    if not query.strip():
        return {
            "answer": "Jeg fant ingen relevant informasjon i dokumentene.",
            "sources": []
        }

    # 1. Lag embedding av query
    query_embedding = create_embedding(query)
    query_vector = np.array(query_embedding, dtype=np.float32).reshape(1, -1)


    # 2. Søk i vector store
    results = vector_store.search(query_vector, top_k=top_k)

    # 3. Bygg prompt
    context = "\n\n".join([r["text"] for r in results])
    """[r["text"] for r in results] her blir lagt en liste som har tekstene fra hvert r dict i results
    .join setter dem sammen til en streng ved hjelp av linjeskift og en tom linje mellom chunkene
    """

    prompt = f"""Du er en hjelpsom assistent.
    Svar kun basert på konteksten nedenfor.

    Kontekst:
    {context}

    Spørsmål:
    {query}
    """


    # 4. Spør språkmodellen
    client = get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content


    # 5. Returner svar + kilder
    return {
        "answer": answer,
        "sources": results
    }

