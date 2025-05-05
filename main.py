
from config_reader import get_config
from dahua_lpr_client import fetch_last_snapshot
from db_writer import save_plate_event
import time

def main():
    config = get_config()
    print("Obteniendo imagen desde cámara...")
    img_path = fetch_last_snapshot(config)
    if img_path:
        print(f"Imagen guardada en: {img_path}")
        fake_plate = "ABC123"  # Simulación de patente detectada
        save_plate_event(fake_plate, img_path)
        print(f"Evento guardado en base de datos: {fake_plate}")
    else:
        print("No se pudo capturar la imagen")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(10)
