from fastapi import HTTPException
from typing import Any
import requests
import json

from app.config.variables import URL_MOTOR

class MotorService:
    @staticmethod
    def create_draft(draft_data: Any):
        url = f"{URL_MOTOR}/reversals"
        response = requests.post(url, json=draft_data)
        
        if response.status_code not in [200, 201]:
            raise HTTPException(status_code=response.status_code, detail=json.loads(response.content))
        
        return response.content.decode()