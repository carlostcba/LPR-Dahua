import os
import requests
from datetime import datetime
from config_reader import get_config

def ensure_folder_exists(folder_path):
    """Asegura que el folder de destino exista"""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def download_and_save_image(image_url, plate, timestamp):
    """Descarga una imagen desde la URL y la guarda en el folder configurado"""
    # Obtener configuración
    config = get_config()
    
    # Preparar credenciales para la cámara Dahua
    auth = (config["cam_user"], config["cam_password"])
    
    # Crear estructura de carpetas por fecha
    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    date_folder = dt.strftime('%Y-%m-%d')
    
    # Definir la carpeta de destino
    base_folder = config["images_folder"]
    full_folder_path = os.path.join(base_folder, date_folder)
    ensure_folder_exists(full_folder_path)
    
    # Generar nombre de archivo único
    filename = f"{plate}_{dt.strftime('%H%M%S')}.jpg"
    full_file_path = os.path.join(full_folder_path, filename)
    
    try:
        # Descargar la imagen
        response = requests.get(image_url, auth=auth, timeout=5)
        response.raise_for_status()  # Lanzar excepción si hay error HTTP
        
        # Guardar la imagen en el sistema de archivos
        with open(full_file_path, 'wb') as f:
            f.write(response.content)
        
        # Devolver la ruta relativa (desde la carpeta base)
        return os.path.join(date_folder, filename)
    
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la imagen: {e}")
        return None
