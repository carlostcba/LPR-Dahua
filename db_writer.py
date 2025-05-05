
import pyodbc
from datetime import datetime

def save_plate_event(plate_number, image_path):
    conn = pyodbc.connect(
        "Driver={SQL Server};Server=localhost;Database=tu_basededatos;UID=usuario;PWD=clave;")
    cursor = conn.cursor()
    timestamp = datetime.now()
    cursor.execute("""
        INSERT INTO LPR_Events (PlateNumber, EventTime, ImagePath)
        VALUES (?, ?, ?)""",
        plate_number, timestamp, image_path
    )
    conn.commit()
    conn.close()
