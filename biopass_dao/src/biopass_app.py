import tkinter as tk
from tkinter import messagebox
import cv2
from usuario_dao import UsuarioDAO
import numpy as np
from utils.camera_utils import image_to_bytes, bytes_to_image

class BioPassApp:
    def __init__(self, master):
        self.master = master
        self.master.title("BioPass DAO")
        self.master.geometry("400x200")

        tk.Label(master, text="Nombre:").pack(pady=5)
        self.nombre_entry = tk.Entry(master)
        self.nombre_entry.pack(pady=5)

        self.registrar_btn = tk.Button(master, text="Registrar Usuario", command=self.registrar_usuario)
        self.registrar_btn.pack(pady=10)

        self.login_btn = tk.Button(master, text="Entrar (Reconocimiento)", command=self.login_usuario)
        self.login_btn.pack(pady=10)

    def capturar_foto(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "No se pudo abrir la cámara")
            return None

        ret, frame = cap.read()
        cap.release()
        if not ret:
            messagebox.showerror("Error", "No se pudo capturar la imagen")
            return None

        # Opcional: mostrar la imagen capturada antes de guardar
        cv2.imshow("Foto Capturada", frame)
        cv2.waitKey(1000)  # 1 segundo
        cv2.destroyAllWindows()

        return frame

    def registrar_usuario(self):
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showwarning("Aviso", "Debes ingresar un nombre")
            return

        foto = self.capturar_foto()
        if foto is None:
            return

        foto_bytes = image_to_bytes(foto)
        success = UsuarioDAO.registrar_usuario(nombre, foto_bytes)
        if success:
            messagebox.showinfo("Éxito", f"Usuario '{nombre}' registrado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo registrar el usuario")

    def login_usuario(self):
        usuarios = UsuarioDAO.obtener_todos()
        if not usuarios:
            messagebox.showinfo("Info", "No hay usuarios registrados")
            return

        foto_actual = self.capturar_foto()
        if foto_actual is None:
            return

        foto_actual_gray = cv2.cvtColor(foto_actual, cv2.COLOR_BGR2GRAY)
        recognizer = cv2.face.LBPHFaceRecognizer_create()

        # Entrenar con todas las fotos de la base
        ids = []
        fotos = []
        for u in usuarios:
            id_usuario, nombre, foto_bytes = u
            img = bytes_to_image(foto_bytes)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            fotos.append(img_gray)
            ids.append(id_usuario)

        if fotos:
            recognizer.train(fotos, np.array(ids))
            id_pred, conf = recognizer.predict(foto_actual_gray)
            nombre_pred = next((u[1] for u in usuarios if u[0] == id_pred), "Desconocido")
            messagebox.showinfo("Resultado", f"Usuario reconocido: {nombre_pred}\nConfianza: {conf:.2f}")
        else:
            messagebox.showinfo("Info", "No hay imágenes para entrenar el modelo")

if __name__ == "__main__":
    root = tk.Tk()
    app = BioPassApp(root)
    root.mainloop()
