import pyodbc
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='lpr_middleware.log'
)
logger = logging.getLogger('db_access')

def get_connection():
    """Obtiene una conexión a la base de datos MSSQL"""
    try:
        return pyodbc.connect("DSN=LPR_MSSQL")
    except pyodbc.Error as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        raise

def is_plate_authorized(plate):
    """
    Verifica si una placa está autorizada en la base de datos.
    
    Args:
        plate (str): Número de placa a verificar
        
    Returns:
        bool: True si la placa está autorizada, False en caso contrario
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Habilitado FROM PatentesAutorizadas WHERE Patente = ?", plate)
        row = cursor.fetchone()
        conn.close()
        
        authorized = row is not None and row.Habilitado == 1
        logger.info(f"Verificación de placa {plate}: {'Autorizada' if authorized else 'No autorizada'}")
        return authorized
    except Exception as e:
        logger.error(f"Error al verificar la placa {plate}: {e}")
        return False

def log_event(plate, timestamp, image_url, status, local_image_path=None):
    """
    Registra un evento LPR en la base de datos.
    
    Args:
        plate (str): Número de placa detectada
        timestamp (str): Marca de tiempo ISO 8601
        image_url (str): URL de la imagen en la cámara
        status (str): Estado del evento (AUTORIZADO/DENEGADO)
        local_image_path (str, optional): Ruta local donde se guardó la imagen
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO LPR_Logs (PlateNumber, EventTime, ImageURL, Status, LocalImagePath)
            VALUES (?, ?, ?, ?, ?)
        """, plate, timestamp, image_url, status, local_image_path)
        conn.commit()
        conn.close()
        logger.info(f"Evento registrado: Placa={plate}, Estado={status}, Imagen={local_image_path}")
    except Exception as e:
        logger.error(f"Error al registrar evento para placa {plate}: {e}")
