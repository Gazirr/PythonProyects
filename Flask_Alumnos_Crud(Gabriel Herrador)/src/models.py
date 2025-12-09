from .db import db

class Alumno(db.Model):
    __tablename__ = 'alumnos'

    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(150), nullable = False)
    apellido = db.Column(db.String(150), nullable = False)
    edad = db.Column(db.Integer, nullable = False)

    def to_dict(self):
        return{
            "id" : self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "edad": self.edad
        }