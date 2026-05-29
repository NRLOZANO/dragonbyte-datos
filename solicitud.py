import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("API_BASE_URL", "http://localhost:8080") + "/api/cursos"
response = requests.get(url)
if response.status_code == 200:
    datos = response.json()
    print("Petición exitosa.")
    print("Tipo de datos recibidos:", type(datos))
    print("Contenido de los datos:", datos)
    df = pd.DataFrame(datos)
    print("DataFrame:")
    print(df)
else:
    print(f"Error en la petición: {response.status_code}")
