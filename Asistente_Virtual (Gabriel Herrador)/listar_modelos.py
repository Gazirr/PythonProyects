import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

# Listar modelos disponibles
for modelo in genai.list_models():
    if "generateContent" in modelo.supported_generation_methods:
        print(modelo.name)
