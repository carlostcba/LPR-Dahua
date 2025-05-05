import os
import requests
from datetime import datetime
import logging
from config_reader import get_config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='lpr_middleware.log'
)
logger = logging.getLogger('image_handler')

def ensure_folder_exists(folder_path):
    """
    Asegura que el folder de destino exista, creándolo si es necesario.
    
    Args:
        folder_path (str): Ruta de la carpeta a verificar/crear
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logger.info(f"Carpeta creada: {folder_path}")

def download_and_save_image(image_url, plate, timestamp):
    """
    Descarga una imagen desde la URL y la guarda en el folder configurado.
    
    Args:
        image_url (str): URL de la imagen a descargar
        plate (str): Número de placa detectada
        timestamp (str): Marca de tiempo ISO 8601
    
    Returns:
        str or None: Ruta relativa donde se guardó la imagen, o None si falló
    """
    try:
        # Obtener configuración
        config = get_config()
        
        # Preparar credenciales para la cámara Dahua
        auth = (config["cam_user"], config["cam_password"])
        
        # Verificar si image_url es una URL completa o solo una ruta parcial
        if not image_url.startswith("http"):
            # Construir URL completa usando snapshot_path o cam_ip
            if config["snapshot_path"]:
                image_url = f"{config['snapshot_path']}/{image_url.lstrip('/')}"
            else:
                image_url = f"http://{config['cam_ip']}/{image_url.lstrip('/')}"
        
        logger.info(f"URL de imagen a descargar: {image_url}")
            
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
        
        # Descargar la imagen
        response = requests.get(image_url, auth=auth, timeout=5)
        response.raise_for_status()  # Lanzar excepción si hay error HTTP
        
        # Guardar la imagen en el sistema de archivos
        with open(full_file_path, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"Imagen guardada correctamente: {full_file_path}")
        
        # Devolver la ruta relativa (desde la carpeta base)
        return os.path.join(date_folder, filename)
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al descargar la imagen: {e}")
        return None
    except Exception as e:
        logger.error(f"Error inesperado al procesar la imagen: {e}")
        return None
