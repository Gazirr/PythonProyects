import csv

notas_uf1_uf2 = {}


with open('Notas_Alumnos_UF1.csv', newline='', encoding='utf-8') as notas1:
    reader = csv.DictReader(notas1, delimiter=';')
    reader.fieldnames = [fn.replace('\ufeff', '').strip() for fn in reader.fieldnames]
    for row in reader:
        row = {k.strip(): v.strip() for k, v in row.items()}
        alumno_id = row['Id']
        notas_uf1_uf2[alumno_id] = {
            'Id': alumno_id,
            'Nombre': row['Nombre'],
            'Apellido': row['Apellidos'],
            'Nota_UF1': row['UF1'],
            'Nota_UF2': ''
        }


with open('Notas_Alumnos_UF2.csv', newline='', encoding='utf-8') as notas2:
    reader = csv.DictReader(notas2, delimiter=';')
    reader.fieldnames = [fn.replace('\ufeff', '').strip() for fn in reader.fieldnames]
    for row in reader:
        row = {k.strip(): v.strip() for k, v in row.items()}
        alumno_id = row['Id']
        if alumno_id in notas_uf1_uf2:

            notas_uf1_uf2[alumno_id]['Nota_UF2'] = row['UF2']
        else:
            notas_uf1_uf2[alumno_id] = {
                'Id': alumno_id,
                'Nombre': row['Nombre'],
                'Apellido': row['Apellidos'],
                'Nota_UF1': '',
                'Nota_UF2': row['UF2']
            }

with open('notas_alumnos.csv', 'w', newline='', encoding='utf-8') as salida:
    campos = ['Id', 'Nombre', 'Apellido', 'Nota_UF1', 'Nota_UF2']
    writer = csv.DictWriter(salida, fieldnames=campos)
    writer.writeheader()
    for alumno in notas_uf1_uf2.values():
        writer.writerow(alumno)
