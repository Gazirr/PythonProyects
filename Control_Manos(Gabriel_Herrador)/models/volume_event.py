from datetime import datetime

class VolumeEvent:
    def __init__(self, vol_percent, distancia):
        self.timestamp = datetime.now()
        self.volumen_nuevo = vol_percent
        self.distancia_dedos = distancia

    def to_dict(self):
        """Convierte el objeto a diccionario para MongoDB"""
        return {
            "timestamp": self.timestamp,
            "volumen_nuevo": self.volumen_nuevo,
            "distancia_dedos": self.distancia_dedos
        }