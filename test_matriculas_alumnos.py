from dominio.alumno import Alumno
from servicio.alumnios_matriculados import AlumnosMatriculados

def menu():
    while True:
        print("\n--- Menu De Matriculas Alumnos ---")
        print("1 - Matriculas Alumnos")
        print("2 - Listar Alumnos")
        print("3 - Eliminar archivo de alumnos")
        print("4 - Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
                nombre = input("Ingrese el nombre deL alumno: ")
                alumno = Alumno(nombre)
                AlumnosMatriculados.matricula_alumnos(alumno)
                print(f"Alumno: '{nombre}' matriculado")
        elif opcion == "2":
            alumnos = AlumnosMatriculados.listar_alumnos()
            if alumnos:
                print("Alumnos Matriculados: ")
                for alumno in alumnos:
                    print(f"- {alumno.strip()}")
            else:
                print("No hay alumnos matriculados")
        elif opcion == "3":
            AlumnosMatriculados.eliminar_alumno()
            print("Archivo de alumnos eliminado")
        elif opcion == "4":
            print("Saliendo del programa")
            break

        else:
            print("Opcion no valida. Intente de Nuevo")


if __name__ == "__main__":
    menu()
