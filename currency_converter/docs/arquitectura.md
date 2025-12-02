El proyecto se divide en capas:

1. Capa API (api/ecb_api.py):
   - Descarga el XML del BCE.
   - Extrae la fecha y las tasas de cada moneda.
   - Devuelve un diccionario con los valores.

2. Capa Lógica (logic/converter.py):
   - Realiza la conversión cruzada usando el euro como base.

3. Capa GUI (gui/main_window.py):
   - Interfaz desarrollada con Tkinter.
   - Recoge la entrada del usuario y muestra el resultado.

4. app.py:
   - Punto de entrada de la aplicación.
