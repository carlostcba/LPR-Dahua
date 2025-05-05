import pyodbc
from datetime import datetime

def get_connection():
    return pyodbc.connect("DSN=LPR_MSSQL")

def is_plate_authorized(plate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Habilitado FROM PatentesAutorizadas WHERE Patente = ?", plate)
    row = cursor.fetchone()
    conn.close()
    return row is not None and row.Habilitado == 1

def log_event(plate, timestamp, image_url, status, local_image_path=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO LPR_Logs (PlateNumber, EventTime, ImageURL, Status, LocalImagePath)
        VALUES (?, ?, ?, ?, ?)
    """, plate, timestamp, image_url, status, local_image_path)
    conn.commit()
    conn.close()
