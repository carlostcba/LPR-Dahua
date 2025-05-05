
# Dahua LPR Middleware (Push Mode)

Este middleware en Python permite recibir eventos en tiempo real desde cámaras Dahua LPR mediante HTTP POST. Evalúa si la patente detectada está autorizada y registra el resultado en una base de datos MSSQL.

## Características

- Recibe eventos ANPR en formato JSON (modo push).
- Consulta una tabla `PatentesAutorizadas` para determinar si se permite el acceso.
- Guarda logs de eventos en `LPR_Logs`.
- Soporta múltiples cámaras simultáneamente (FastAPI asincrónico).
- Tiempo de reacción en milisegundos.

## Requisitos

- Python 3.10+
- MSSQL Server
- FastAPI + Uvicorn
- Red LAN entre cámara y servidor

## Instalación

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Base de datos

```sql
CREATE TABLE PatentesAutorizadas (
    id INT PRIMARY KEY IDENTITY,
    Patente VARCHAR(20) UNIQUE,
    Habilitado BIT,
    Observaciones VARCHAR(255)
);

CREATE TABLE LPR_Logs (
    Id INT IDENTITY PRIMARY KEY,
    PlateNumber VARCHAR(20),
    EventTime DATETIME,
    ImageURL VARCHAR(255),
    Status VARCHAR(20)
);
```

## Configuración de cámaras Dahua

Configurar cada cámara para enviar eventos ANPR vía HTTP POST a:

```
http://[IP_DEL_SERVIDOR]:8000/evento-lpr
```

Formato del cuerpo (JSON):
```json
{
  "plate": "ABC123",
  "timestamp": "2025-05-05T12:34:56Z",
  "image_url": "http://[cam_ip]/snapshot.jpg"
}
```

## Integración con relés u otros sistemas

Dentro de `receive_lpr_event` podés integrar lógica adicional como:
- Enviar señal a GPIO
- Activar HTTP GET/POST a otro servicio
- Controlar hardware conectado a Raspberry Pi, Arduino, etc.

