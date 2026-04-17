from .client import get_client

def create_embedding (text: str) -> list[float]:

    #Tar imot tekst og returnerer embedding-vektoren.

    client = get_client()

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    # Hent selve vektoren
    vector = response.data[0].embedding

    return vector

def embed_chunks(chunks: list, source: str) -> list:
    """
    Tar imot en liste med tekst-chunks og lager embeddings med metadata.
    """
    if not chunks:
        return []
    
    embedded_chunks = []
    

    for i, chunk in enumerate(chunks):
        embedding = create_embedding(chunk)
        chunk_data = {}
        chunk_data ["id"] = i
        chunk_data ["text"] = chunk
        chunk_data ["embedding"] = embedding
        chunk_data ["metadata"] = {"source" : source, "chunk_index": i}

        embedded_chunks.append(chunk_data)

    return embedded_chunks