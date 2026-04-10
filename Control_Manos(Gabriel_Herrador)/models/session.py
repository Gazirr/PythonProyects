from datetime import datetime

class Session:
    def __init__(self, usuario):
        self.usuario = usuario
        self.inicio = datetime.now()
        self.fin = None
        self.estado = "activa"

    def to_dict(self):
        """Convierte el objeto a diccionario para MongoDB"""
        return {
            "usuario": self.usuario,
            "inicio": self.inicio,
            "fin": self.fin,
            "estado": self.estado
        }