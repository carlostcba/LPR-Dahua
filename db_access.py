
import pyodbc

def get_connection():
    return pyodbc.connect(
        "Driver={SQL Server};Server=localhost;Database=tu_basededatos;UID=usuario;PWD=clave;"
    )

def is_plate_authorized(plate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Habilitado FROM PatentesAutorizadas WHERE Patente = ?", plate)
    row = cursor.fetchone()
    conn.close()
    return row is not None and row.Habilitado == 1

def log_event(plate, timestamp, image_url, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO LPR_Logs (PlateNumber, EventTime, ImageURL, Status)
        VALUES (?, ?, ?, ?)
    """, plate, timestamp, image_url, status)
    conn.commit()
    conn.close()
