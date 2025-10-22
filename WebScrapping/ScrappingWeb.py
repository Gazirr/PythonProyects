import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.worldometers.info/world-population/population-by-country/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Prueba buscar las tablas y ver si alguna tiene filas
tables = soup.find_all("table")
print(f"Se encontraron {len(tables)} tablas.")

for i, tbl in enumerate(tables):
    print(f"Tabla {i} id:", tbl.get("id"))
    # Puedes imprimir algunas filas para ver qué contiene
    first_row = tbl.find("tr")
    if first_row:
        print("Primera fila:", first_row.text.strip()[:100])

# Elegimos la primera tabla con filas como ejemplo
table = tables[0]  # o usa otro índice si quieres

# Ahora sí, extraemos encabezados y filas
headers = [th.text.strip() for th in table.find_all("th")]

rows = []
for tr in table.find("tbody").find_all("tr"):
    cells = tr.find_all("td")
    row = [cell.text.strip() for cell in cells]
    rows.append(row)

df = pd.DataFrame(rows, columns=headers)
df.to_csv("paises_poblacion.csv", index=False, encoding='utf-8')

print("✅ Datos guardados exitosamente en 'paises_poblacion.csv'")
