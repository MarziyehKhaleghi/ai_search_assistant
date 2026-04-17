import os
#os gir funksjoner som lar Python snakke med operativsystemet
import pdfplumber  # lese PDF
import docx   # lese Word-dokumenter


def load_text_file(file_path: str) -> str:
    #Laster inn en .txt-fil og returnerer innholdet som en streng.
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Finner ikke filen: {file_path}")
    
    if not file_path.lower().endswith(".txt"):
        raise ValueError("Dette er ikke en .txt-fil.")
    
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()
    
    
def load_pdf_file(file_path):
     
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Finner ikke filen: {file_path}")
     
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text
    

def load_docx_file(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Finner ikke filen: {file_path}")

    document = docx.Document(file_path)
    full_text = ""
    for paragraph in document.paragraphs:
        text = paragraph.text
        if text != "":
            full_text += text + "\n"
    
    return full_text


def load_document(file_path: str) -> str:
    """
    Laster dokument basert på filtype.
    Støtter foreløpig kun .txt, men vil utvides med PDF og DOCX senere.
    """

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".txt":
        return load_text_file(file_path)
    elif ext == ".pdf":
        return load_pdf_file(file_path)
    elif ext == ".docx":
        return load_docx_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")



