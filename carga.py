import requests
import pandas as pd
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv ( "API_BASE_URL") 

def cargar_archivo (endpoint: str) -> pd.DataFrame:
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url)
    response.raise_for_status()
    return pd.DataFrame(response.json())

def get_cursos() -> pd.DataFrame:
   return cargar_archivo("/api/cursos")


def get_usuarios() -> pd.DataFrame:
    return cargar_archivo("/api/usuarios")

