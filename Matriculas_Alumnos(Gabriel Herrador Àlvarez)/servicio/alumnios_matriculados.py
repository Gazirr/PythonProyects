from dominio.alumno import Alumno

class AlumnosMatriculados:
    ruta_archivo = "alumnos.txt"

    @staticmethod
    def matricula_alumnos(alumno: Alumno):
            with open(AlumnosMatriculados.ruta_archivo, "a", encoding="utf-8") as archivo:
                archivo.write(f"{alumno.nombre}\n")


    @staticmethod
    def listar_alumnos():
        try:
            with open(AlumnosMatriculados.ruta_archivo, "r", encoding="utf-8") as archivo:
                return archivo.readlines()
        except FileNotFoundError:
            return []

    @staticmethod
    def eliminar_alumno():
        import os
        if os.path.exists(AlumnosMatriculados.ruta_archivo):
            os.remove(AlumnosMatriculados.ruta_archivo)