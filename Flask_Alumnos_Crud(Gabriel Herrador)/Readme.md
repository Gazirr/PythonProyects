# Actividad Crud Alumnos:
Esta actividad es una version de un CRUD basico con Python y fastApi
# Comandos Crud:

# Get List:
 Basicamente el comando de abajo lo que hace es traerte la lista de los Alumnos.

- Invoke-RestMethod "http://127.0.0.1:5000/api/alumnos" -Method GET

# Get (un Alumno):
 Basicamente el comando de abajo lo que hace es traerte a un Alumno en concreto.

- Invoke-RestMethod "http://127.0.0.1:5000/api/alumnos/1" -Method GET

# POST :
 Baicamente lo que hace es añadir  un alumno y guardarlo.

- Invoke-RestMethod "http://127.0.0.1:5000/api/alumnos" -Method POST -ContentType "application/json" -Body (@{nombre="Daniel";apellido="Zorita";edad=19} | ConvertTo-Json)

# PUT (Actualizar un alumno):
 Basicamente lo que hace es actualizar un Alumno.

- Invoke-RestMethod "http://127.0.0.1:5000/api/alumnos/1" -Method PUT -ContentType "application/json" -Body (@{nombre="Daniel";apellido="Zorita";edad=20} | ConvertTo-Json)

# DELETE (Elimina un alumno):
 Basicamente lo que hace es eliminar un Alumno.
- Invoke-RestMethod "http://127.0.0.1:5000/api/alumnos/1" -Method DELETE

