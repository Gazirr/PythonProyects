import tkinter as tk
from tkinter import messagebox, scrolledtext
from auth_dao import AuthDAO
from voice_service import VoiceService
from datetime import datetime

class VoiceAuditApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VoiceAudit Login System")
        self.root.geometry("600x500")
        
        self.auth_dao = AuthDAO()
        self.voice_service = VoiceService()
        
        self.setup_ui()

    def setup_ui(self):
        # Header
        tk.Label(self.root, text="VoiceAudit Login", font=("Helvetica", 18, "bold")).pack(pady=10)
        
        # User input
        tk.Label(self.root, text="Nombre de usuario:").pack()
        self.entry_username = tk.Entry(self.root, width=30)
        self.entry_username.pack(pady=5)
        
        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Registrar (Enrolamiento)", command=self.enroll, bg="lightblue").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Iniciar Sesión", command=self.login, bg="lightgreen").grid(row=0, column=1, padx=5)
        tk.Button(self.root, text="Ver Panel de Auditoría Crítica", command=self.show_audit).pack(pady=5)
        
        # Output info
        tk.Label(self.root, text="Consola de Estado:").pack()
        self.console = scrolledtext.ScrolledText(self.root, height=10, width=70)
        self.console.pack(pady=10)

    def log_console(self, message):
        self.console.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.console.see(tk.END)

    def enroll(self):
        username = self.entry_username.get().strip()
        if not username:
            messagebox.showwarning("Aviso", "Introduce un nombre de usuario.")
            return

        self.log_console(f"Iniciando enrolamiento para {username}...")
        texto, confianza, latencia, error = self.voice_service.listen_and_recognize()
        
        if error:
            self.log_console(f"Error: {error}")
            return
        
        self.log_console(f"Frase reconocida: '{texto}'")
        if messagebox.askyesno("Confirmar Frase", f"¿Es esta tu frase secreta?\n\n'{texto}'"):
            result_json = {"status": "OK", "confianza": confianza, "latencia": f"{latencia}s"}
            if self.auth_dao.register_user(username, texto, result_json):
                messagebox.showinfo("Éxito", f"Usuario {username} registrado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo registrar al usuario.")
        else:
            self.log_console("Registro cancelado por el usuario.")

    def login(self):
        username = self.entry_username.get().strip()
        if not username:
            messagebox.showwarning("Aviso", "Introduce un nombre de usuario.")
            return

        user_data = self.auth_dao.get_user_by_username(username)
        if not user_data:
            messagebox.showerror("Error", "Usuario no encontrado.")
            return

        user_id, _, saved_passphrase, fallidos, bloqueado_hasta = user_data
        
        # Verificar bloqueo
        if bloqueado_hasta and datetime.now() < bloqueado_hasta:
            messagebox.showwarning("Bloqueado", f"Usuario bloqueado hasta {bloqueado_hasta}")
            return

        self.log_console(f"Escuchando frase de paso para {username}...")
        texto, confianza, latencia, error = self.voice_service.listen_and_recognize()

        if error:
            self.log_console(f"Error: {error}")
            self.auth_dao.login_attempt(user_id, "ERROR", {"motivo": error})
            return

        self.log_console(f"Frase escuchada: '{texto}' (Confianza: {confianza})")
        
        if texto.lower() == saved_passphrase.lower():
            self.log_console("Acceso CONCEDIDO.")
            self.auth_dao.login_attempt(user_id, "OK", {"confianza": confianza, "latencia": f"{latencia}s"})
            messagebox.showinfo("Acceso", "¡Bienvenido!")
        else:
            self.log_console("Acceso DENEGADO (Frase incorrecta).")
            intentos_restantes = 2 - fallidos # 3 intentos total
            self.auth_dao.login_attempt(user_id, "FAIL", {
                "frase_intentada": texto, 
                "intentos_restantes": max(0, intentos_restantes)
            })
            messagebox.showwarning("Fallo", f"Frase incorrecta. Intentos restantes: {max(0, intentos_restantes)}")

    def show_audit(self):
        logs = self.auth_dao.get_critical_logs()
        audit_window = tk.Toplevel(self.root)
        audit_window.title("Panel de Auditoría Crítica (JSONB Query)")
        audit_window.geometry("500x400")
        
        text_area = scrolledtext.ScrolledText(audit_window, width=60, height=20)
        text_area.pack(padx=10, pady=10)
        
        if not logs:
            text_area.insert(tk.END, "No hay registros críticos detectados.")
        else:
            for username, fecha, res_json in logs:
                line = f"[{fecha}] USER: {username} | {res_json}\n"
                text_area.insert(tk.END, line)
        
        text_area.configure(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAuditApp(root)
    root.mainloop()
