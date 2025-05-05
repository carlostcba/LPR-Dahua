from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from db_access import is_plate_authorized, log_event
from image_handler import download_and_save_image
from fastapi.responses import JSONResponse
import uvicorn
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='lpr_middleware.log'
)
logger = logging.getLogger('main')

app = FastAPI(title="Dahua LPR Middleware")

class LPREvent(BaseModel):
    plate: str
    timestamp: str
    image_url: str

@app.post("/evento-lpr")
async def receive_lpr_event(event: LPREvent):
    """
    Endpoint que recibe eventos LPR desde cámaras Dahua.
    
    Args:
        event (LPREvent): Evento LPR con placa, timestamp y URL de imagen
        
    Returns:
        JSONResponse: Respuesta con estado de autorización e imagen local
    """
    try:
        logger.info(f"Evento recibido: Placa={event.plate}, Timestamp={event.timestamp}")
        
        # Verificar si la placa está autorizada
        authorized = is_plate_authorized(event.plate)
        action = "AUTORIZADO" if authorized else "DENEGADO"
        
        # Descargar y guardar la imagen
        local_image_path = download_and_save_image(
            event.image_url, 
            event.plate, 
            event.timestamp
        )
        
        # Si falló la descarga de la imagen, registrar aviso
        if local_image_path is None:
            logger.warning(f"No se pudo guardar la imagen para la placa {event.plate}")
        
        # Registrar el evento en la base de datos
        log_event(
            event.plate, 
            event.timestamp, 
            event.image_url, 
            action,
            local_image_path
        )

        # Aquí podrías accionar un relé, enviar señal, etc.
        # if authorized:
        #     # Código para activar relé u otra acción
        
        response_data = {
            "status": action,
            "local_image": local_image_path
        }
        
        return JSONResponse(content=response_data, status_code=200)
    
    except Exception as e:
        logger.error(f"Error al procesar evento LPR: {e}")
        return HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Endpoint para verificar que el servicio está funcionando"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
