import pyodbc

def get_config():
    """
    Obtiene la configuración de la cámara desde la base de datos.
    
    Returns:
        dict: Diccionario con configuración de la cámara (IP, credenciales, paths)
    """
    conn = pyodbc.connect("DSN=LPR_MSSQL")
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 cam_ip, cam_user, cam_password, snapshot_path, images_folder FROM DahuaConfig ORDER BY id")
    row = cursor.fetchone()
    conn.close()
    
    # Si images_folder no está definido, usar un valor predeterminado
    images_folder = row.images_folder if row.images_folder else "C:\\LPR_Images"
    
    return {
        "cam_ip": row.cam_ip,
        "cam_user": row.cam_user,
        "cam_password": row.cam_password,
        "snapshot_path": row.snapshot_path,  # Base URL de la cámara para construir URLs de imágenes si es necesario
        "images_folder": images_folder       # Carpeta local donde se guardarán las imágenes
    }
