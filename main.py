
from fastapi import FastAPI, Request
from pydantic import BaseModel
from db_access import is_plate_authorized, log_event
from fastapi.responses import JSONResponse
from datetime import datetime
import uvicorn

app = FastAPI()

class LPREvent(BaseModel):
    plate: str
    timestamp: str
    image_url: str

@app.post("/evento-lpr")
async def receive_lpr_event(event: LPREvent):
    authorized = is_plate_authorized(event.plate)
    action = "AUTORIZADO" if authorized else "DENEGADO"
    
    log_event(event.plate, event.timestamp, event.image_url, action)

    # Aquí podrías accionar un relé, enviar señal, etc.
    return JSONResponse(content={"status": action}, status_code=200)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
