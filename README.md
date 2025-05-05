
# Dahua LPR Middleware

Este proyecto en Python permite capturar imágenes de una cámara Dahua con autenticación Digest y almacenar los eventos (patente, hora, imagen) en una base de datos MSSQL.

## Requisitos

- Python 3.10+
- MSSQL con tabla `LPR_Events`
- Configuración previa de cámara Dahua (modelo ITC431-RW1F-IRL8)

## Estructura del proyecto

- `main.py`: Loop principal que ejecuta la lectura cada 10 segundos.
- `config_reader.py`: Obtiene IP, usuario y ruta desde la base de datos.
- `dahua_lpr_client.py`: Captura una imagen usando Digest Auth.
- `db_writer.py`: Guarda el evento en MSSQL.
- `requirements.txt`: Librerías necesarias.

## Instalación

```bash
pip install -r requirements.txt
python main.py
```

## Compilar a EXE

```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

El `.exe` estará en la carpeta `dist/`.

## Tabla SQL esperada

```sql
CREATE TABLE DahuaConfig (
    id INT PRIMARY KEY,
    cam_ip VARCHAR(100),
    cam_user VARCHAR(50),
    cam_password VARCHAR(50),
    snapshot_path VARCHAR(255)
);

CREATE TABLE LPR_Events (
    Id INT IDENTITY PRIMARY KEY,
    PlateNumber VARCHAR(20),
    EventTime DATETIME,
    ImagePath VARCHAR(255)
);
```
