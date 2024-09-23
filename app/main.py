from fastapi import FastAPI
from app.controllers import request_controller

app = FastAPI()

# Registrar las rutas
app.include_router(request_controller.router)

# Inicia el servidor con: uvicorn app.main:app --reload
