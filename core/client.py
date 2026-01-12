from openai import OpenAI
from .config import OPENAI_API_KEY


def get_client():
    """
    Returnerer en OpenAI-klient konfigurert med API-nøkkelen vår.
    Dette gjør at alle andre moduler kan hente en klient når de trenger det.
    """
    return OpenAI(api_key=OPENAI_API_KEY)

