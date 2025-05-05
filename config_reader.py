
import pyodbc

def get_config():
    conn = pyodbc.connect(
        "Driver={SQL Server};Server=localhost;Database=tu_basededatos;UID=usuario;PWD=clave;"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 cam_ip, cam_user, cam_password, snapshot_path FROM DahuaConfig ORDER BY id")
    row = cursor.fetchone()
    conn.close()
    return {
        "cam_ip": row.cam_ip,
        "cam_user": row.cam_user,
        "cam_password": row.cam_password,
        "snapshot_path": row.snapshot_path
    }
