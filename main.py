from fastapi import FastAPI, Request
from pydantic import BaseModel
from db_access import is_plate_authorized, log_event
from image_handler import download_and_save_image
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

class LPREvent(BaseModel):
    plate: str
    timestamp: str
    image_url: str

@app.post("/evento-lpr")
async def receive_lpr_event(event: LPREvent):
    # Verificar si la placa está autorizada
    authorized = is_plate_authorized(event.plate)
    action = "AUTORIZADO" if authorized else "DENEGADO"
    
    # Descargar y guardar la imagen
    local_image_path = download_and_save_image(
        event.image_url, 
        event.plate, 
        event.timestamp
    )
    
    # Registrar el evento en la base de datos
    log_event(
        event.plate, 
        event.timestamp, 
        event.image_url, 
        action,
        local_image_path
    )

    # Aquí podrías accionar un relé, enviar señal, etc.
    response_data = {
        "status": action,
        "local_image": local_image_path
    }
    
    return JSONResponse(content=response_data, status_code=200)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
