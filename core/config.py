#Importer nødvendige pakker
import os 
from dotenv import load_dotenv

#Last inn .env-filen
load_dotenv()  # Dette leser alle variabler fra .env

#Hent OpenAI API-nøkkel fra miljøvariabler
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#Sjekk om nøkkelen finnes
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API-nøkkel ikke funnet. Sjekk .env-filen!")

#Andre innstillinger / konstanter
DATA_PATH = "data/"        # sti til dokumentmappen
CHUNK_SIZE = 500           # hvor stor hver chunk skal være
TOP_K = 3                 # antall relevante resultater som hentes
MODEL_NAME = "text-embedding-3-small"  # hvilken modell som brukes