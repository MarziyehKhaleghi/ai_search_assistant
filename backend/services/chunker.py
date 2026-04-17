import tiktoken

def chunk_text (text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    
    if not text.strip():
        return []
    
    encoding = tiktoken.get_encoding("cl100k_base")
    # encoding er en object av get_encoding funksjonen
    tokens = encoding.encode(text)
    # her bruker encoding objektet encode funksjonen for å encode teksten

    chunk_texts = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]

        # dekoder tokenene tilbake til tekst
        chunk_texts.append(encoding.decode(chunk_tokens))
        
        # flytt start med overlap
        start = start + chunk_size - overlap

    return chunk_texts
