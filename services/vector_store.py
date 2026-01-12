import faiss
import numpy as np

class VectorStore:

    def __init__(self):
        self.index = None
        self.data = {}

    def add (self, chunks: list):
        """
        Tar imot en liste med chunk-dict og legger dem til FAISS-index.
        """
        if not chunks:
            return
        
        # Opprett FAISS-index hvis den ikke finnes
        if self.index is None:
            dim = len(chunks[0]["embedding"])
            self.index = faiss.IndexFlatL2(dim)

        # Legg alle chunks inn i index og self.data
        for chunk in chunks:
            id = chunk["id"]
            embedding = np.array(chunk["embedding"], dtype=np.float32).reshape(1, -1)
            """
            Konverterer Python-listen til et NumPy-array(Numerical Python): effektiv håndtering av store tall-lister (arrays)
            dtype=np.float32 = hver verdi blir en 32-bit flyttall
               -FAISS krever at embeddingene er float32, ikke vanlig Python float (float64)
            FAISS krever at embeddingene kommer inn som 2D-array (rader × kolonner):
               -1 rad = én embedding
               -Antall kolonner = dimensjonen på embedding (f.eks. 1536)
            """
            text = chunk["text"]
            metadata = chunk["metadata"]

            # Legg til i FAISS
            self.index.add(embedding)

            # Legg til i self.data
            self.data[id] = {"text": text, "metadata": metadata}
        

    def search(self, query_embedding: list, top_k: int = 2):
        """
        Søker i FAISS-indexen og returnerer de mest relevante chunkene.
        """
        if self.index is None:
           return []

        if not self.data:
           return []
        
        query_vector = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
        
        distances, indices = self.index.search(query_vector, top_k)
        """Et kall til FAISS search metode og det retunerer (distances, indices)
        """
        
        results = []

        for idx, dist in zip(indices[0], distances[0]):
            # parer elementer
            chunk = self.data.get(idx)
            # Her skjer koblingen mellom: FAISS og data, får data for denne indexen.
            if chunk:
                # sjekker igjen om det finnes, hvis ikke hopper over og ikke krasjer.
                results.append({
                "id": idx,
                "text": chunk["text"],
                "metadata": chunk["metadata"],
                "score": float(dist)       })

        return results


   