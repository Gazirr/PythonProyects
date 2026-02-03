import cv2
import numpy as np

def image_to_bytes(image):
    success, buffer = cv2.imencode(".jpg", image)
    if not success:
        raise ValueError("No se pudo convertir la imagen a bytes")
    return buffer.tobytes()

def bytes_to_image(image_bytes):
    np_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    return image
