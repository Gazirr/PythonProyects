# Biopass Acceso A Datos
BioPass DAO es un sistema de control de acceso biométrico que permite registrar y autenticar usuarios mediante reconocimiento facial. Su enfoque principal no es solo capturar imágenes y compararlas, sino demostrar buenas prácticas de desarrollo profesional usando patrones de diseño.

El proyecto implementa:

DAO (Data Access Object): separa la lógica de negocio de la base de datos. La interfaz nunca interactúa directamente con SQL; todas las consultas pasan por el DAO.

Singleton: asegura que solo exista una única conexión activa a la base de datos, evitando saturar el servidor.

Gestión de BLOBs: las fotos de los usuarios se guardan como datos binarios en PostgreSQL, garantizando que la información esté centralizada y segura.

Interfaz en tiempo real: la aplicación activa la cámara para capturar la cara del usuario en vivo, sin necesidad de seleccionar archivos, y utiliza OpenCV para procesar las imágenes.

Reconocimiento facial: cuando un usuario inicia sesión, la aplicación compara la imagen capturada con todas las fotos registradas, entrenando el modelo LBPH “al vuelo” para predecir quién es.

En pocas palabras: BioPass DAO permite registrar usuarios con su rostro y luego identificarlos automáticamente, todo mientras sigue principios de arquitectura limpia, seguridad y eficiencia en la conexión a datos.
