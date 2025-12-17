import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

with open("servicios.txt", "r", encoding="utf-8") as f:
    CONTEXTO = f.read()

modelo = genai.GenerativeModel("gemini-2.5-flash")

def obtener_respuesta():
    pregunta = entrada_usuario.get("1.0", tk.END).strip()
    if not pregunta:
        return

    prompt = f"""
Eres un asistente virtual para una peluquería.
Usa la siguiente información del negocio para responder:

{CONTEXTO}

Usuario: {pregunta}
"""

    try:
        respuesta = modelo.generate_content(prompt)

        respuesta_json = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": respuesta.text
                            }
                        ]
                    }
                }
            ]
        }

        texto_respuesta = respuesta_json["candidates"][0]["content"]["parts"][0]["text"]

        salida_texto.config(state="normal")
        salida_texto.insert(tk.END, f"Usuario: {pregunta}\n")
        salida_texto.insert(tk.END, f"Asistente: {texto_respuesta}\n\n")
        salida_texto.config(state="disabled")

        entrada_usuario.delete("1.0", tk.END)

    except Exception as e:
        salida_texto.config(state="normal")
        salida_texto.insert(tk.END, f"[Error] {str(e)}\n\n")
        salida_texto.config(state="disabled")

ventana = tk.Tk()
ventana.title("Asistente Virtual de Peluquería")
ventana.geometry("600x500")

tk.Label(
    ventana,
    text="Asistente Virtual - Peluquería 'Estilo y Belleza'",
    font=("Arial", 14, "bold")
).pack(pady=10)

salida_texto = scrolledtext.ScrolledText(
    ventana,
    wrap=tk.WORD,
    width=70,
    height=15,
    state="disabled"
)
salida_texto.pack(padx=10, pady=10)

tk.Label(
    ventana,
    text="Escribe tu pregunta:",
    font=("Arial", 11)
).pack()

entrada_usuario = tk.Text(
    ventana,
    height=3,
    width=60
)
entrada_usuario.pack(pady=5)

tk.Button(
    ventana,
    text="Enviar",
    command=obtener_respuesta,
    font=("Arial", 12, "bold")
).pack(pady=10)

ventana.mainloop()
