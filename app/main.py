from fastapi import FastAPI
from app.controllers import res_controller

app = FastAPI()

# Registrar las rutas
app.include_router(res_controller.router)

# Inicia el servidor con: uvicorn app.main:app --reload
