import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

# Cargar contexto desde archivo
with open("servicios.txt", "r", encoding="utf-8") as f:
    CONTEXTO = f.read()

# Crear modelo
modelo = genai.GenerativeModel("gemini-2.5-flash")  # Asegúrate de que este modelo esté disponible

# Función para manejar la consulta del usuario
def obtener_respuesta():
    pregunta = entrada_usuario.get("1.0", tk.END).strip()
    if not pregunta:
        return

    # Crear prompt con contexto
    prompt = f"""
Eres un asistente virtual para una peluquería.
Usa la siguiente información del negocio para responder:

{CONTEXTO}

Usuario: {pregunta}
"""

    try:
        respuesta = modelo.generate_content(prompt)
        texto_respuesta = respuesta.text

        # Mostrar respuesta en la interfaz
        salida_texto.config(state='normal')
        salida_texto.insert(tk.END, f"🧍 Usuario: {pregunta}\n")
        salida_texto.insert(tk.END, f"💇 Asistente: {texto_respuesta}\n\n")
        salida_texto.config(state='disabled')

        # Borrar entrada
        entrada_usuario.delete("1.0", tk.END)

    except Exception as e:
        salida_texto.config(state='normal')
        salida_texto.insert(tk.END, f"[Error] No se pudo obtener respuesta: {e}\n\n")
        salida_texto.config(state='disabled')


# Crear ventana principal
ventana = tk.Tk()
ventana.title("Asistente Virtual de Peluquería 💇‍♀️")
ventana.geometry("600x500")
ventana.config(bg="#f2f2f2")

# Etiqueta
tk.Label(ventana, text="Asistente Virtual - Peluquería 'Estilo y Belleza'",
         font=("Arial", 14, "bold"), bg="#f2f2f2").pack(pady=10)

# Cuadro de salida
salida_texto = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=70, height=15, state='disabled')
salida_texto.pack(padx=10, pady=10)

# Entrada de usuario
tk.Label(ventana, text="Escribe tu pregunta:", bg="#f2f2f2", font=("Arial", 11)).pack()
entrada_usuario = tk.Text(ventana, height=3, width=60)
entrada_usuario.pack(pady=5)

# Botón enviar
boton_enviar = tk.Button(ventana, text="Enviar", command=obtener_respuesta, bg="#4CAF50", fg="white",
                         font=("Arial", 12, "bold"))
boton_enviar.pack(pady=10)

# Ejecutar ventana
ventana.mainloop()
