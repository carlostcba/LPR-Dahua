
import pyodbc

def get_config():
    conn = pyodbc.connect(
        "Driver={SQL Server};Server=localhost;Database=tu_basededatos;UID=usuario;PWD=clave;")
    cursor = conn.cursor()
    cursor.execute("SELECT cam_ip, cam_user, cam_password, snapshot_path FROM DahuaConfig WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    return {
        "ip": row.cam_ip,
        "user": row.cam_user,
        "password": row.cam_password,
        "snapshot_path": row.snapshot_path
    }
