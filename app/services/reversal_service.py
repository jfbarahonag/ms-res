from fastapi import HTTPException
from typing import Any

from app.schemas.request_schema import RequestMaintenanceSchema 
from app.schemas.maintenance_schema import MaintenanceSchema
from app.models.reversal import ReversalType

def validate_type(type:str, value:str):
    return True

class RequestReversalService:
    @staticmethod
    def handle_reversal_request(data: RequestMaintenanceSchema):
        if data.maintenance.subType not in [ReversalType.porErroresCliente, ReversalType.porErroresOperativos]:
            raise HTTPException(status_code=400, detail=f"Tipo de reversion '{data.maintenance.subType}' invalido para reversiones")
        reversal = RequestReversalService.parse_as_reversal(data.maintenance)
        
        return reversal
    
    @staticmethod
    def parse_as_reversal(maintenance: MaintenanceSchema) -> dict[str, Any]:
        output = {}
        output["byOperational"] = {}
        output["byClient"] = {}
        output["type"] = maintenance.subType
        
        for item in maintenance.info:
            if item.key in ["dateOfIncorrectPayment"]:
                if not validate_type(item.type, item.value):
                    raise HTTPException(status_code=400, detail=f"Item '{item.key}' invalido")
                output["byClient"][item.key] = item.value
            elif item.key in ["errors", "correctiveActions"]:
                if not validate_type(item.type, item.value):
                    raise HTTPException(status_code=400, detail=f"Item '{item.key}' invalido")
                output["byOperational"][item.key] = item.value
            
        return output