import faiss
import numpy as np
import os
import pickle

class VectorStore:

    def __init__(self,
                 index_path: str = "data/vector_store.index",
                 metadata_path: str = "data/metadata.pkl",
                 ):
        self.index = None
        self.data = {}
        self.index_path = index_path
        self.metadata_path = metadata_path
        self._load_if_exists()

    def _load_if_exists(self):
        """
        Laster FAISS-index og metadata fra disk hvis begge finnes.
        """
        index_exists = os.path.exists(self.index_path)
        metadata_exists = os.path.exists(self.metadata_path)

        if index_exists and metadata_exists:
            print("🔄 Laster eksisterende FAISS-index og metadata...")
            self.index = faiss.read_index(self.index_path)

            with open(self.metadata_path, "rb") as f:
                self.data = pickle.load(f)

            print(f"✅ Lastet {len(self.data)} chunks fra disk.")
        else:
            print(f"🆕 Ingen eksisterende vector store funnet. Starter tom.")


    def _save(self):
        """
        Lagrer FAISS-index og metadata til disk.
        """
        if self.index is None:
            return
        
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)

        faiss.write_index(self.index, self.index_path)

        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.data, f)

        print("💾 Vector store lagret til disk.")



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

        embeddings = []
        ids = []

        current_index = len(self.data)
        # Legg alle chunks inn i index og self.data
        for chunk in chunks:
            embedding = np.array(chunk["embedding"], dtype=np.float32)
            """
            Konverterer Python-listen til et NumPy-array(Numerical Python): effektiv håndtering av store tall-lister (arrays)
            dtype=np.float32 = hver verdi blir en 32-bit flyttall
               -FAISS krever at embeddingene er float32, ikke vanlig Python float (float64)
            """
            embeddings.append(embedding)
            self.data[current_index] = {
                "text": chunk["text"],
                "metadata": chunk["metadata"],
            }

            current_index += 1

            

        embeddings_np = np.vstack(embeddings)
        """FAISS krever at embeddingene kommer inn som 2D-array (rader × kolonner):
               -1 rad = én embedding
               -Antall kolonner = dimensjonen på embedding (f.eks. 1536)"""
        self.index.add(embeddings_np)

        self._save()

         
         
    def search(self, query_embedding: list, top_k: int = 3):
        """
        Søker i FAISS-indexen og returnerer de mest relevante chunkene.
        """
        if self.index is None or not self.data:
           return []
        
        query_vector = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
        
        distances, indices = self.index.search(query_vector, top_k)
        """Et kall til FAISS search metode og det retunerer (distances, indices)
        """
        
        results = []

        for idx, dist in zip(indices[0], distances[0]):
            #indices[0] = listen med resultater for den første queryen
            # parer elementer
            chunk = self.data.get(idx)
            # Her skjer koblingen mellom: FAISS og data, får data for denne indexen.
            if chunk:
                # sjekker igjen om det finnes, hvis ikke hopper over og ikke krasjer.
                results.append({
                "id": int(idx),
                "text": chunk["text"],
                "metadata": chunk["metadata"],
                "score": float(dist)       
                })

        return results


   