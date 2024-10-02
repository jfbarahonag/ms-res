from datetime import datetime, timedelta
from fastapi import HTTPException

from app.schemas.request_schema import RequestMaintenanceSchema, RequestDraftMaintenanceSchema
from app.schemas.maintenance_schema import MaintenanceSchema, AttachmentsSchema
from app.schemas.reversal_schema import ReversalDataSchema

from app.models.reversal import ReversalType

from app.services.motor_service import MotorService

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def is_date_more_than_N_days(date_str, N=30):
    date_format = "%d/%m/%Y"
    input_date = datetime.strptime(date_str, date_format)
    today = datetime.now()
    limit_date = today - timedelta(days=N)

    return input_date < limit_date


def validate_type(type:str, value:str):
    if type not in ['date', 'text']:
        return False
    if type == 'date':
        return is_valid_date(value)
    return True

class RequestReversalService:
    @staticmethod
    def handle_draft_reversal_request(data: RequestDraftMaintenanceSchema):
        response = MotorService.create_draft(data.model_json_schema())
        return response
    
    @staticmethod
    def handle_reversal_request(data: RequestMaintenanceSchema):
        if data.maintenance.subType not in [ReversalType.porErroresCliente, ReversalType.porErroresOperativos]:
            raise HTTPException(status_code=400, detail=f"Tipo de reversion '{data.maintenance.subType}' invalido para reversiones")
        
        reversal = RequestReversalService.parse_as_reversal(data.maintenance)
        
        RequestReversalService.validate_mandatory_attachments(reversal, data.maintenance.attachments)
        
        response = MotorService.create_draft(reversal.model_json_schema())
        
        return response
    
    @staticmethod
    def parse_as_reversal(maintenance: MaintenanceSchema) -> ReversalDataSchema:
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
            
        return ReversalDataSchema(**output)
    
    @staticmethod
    def validate_mandatory_attachments(reversal: ReversalDataSchema, attachments: list[AttachmentsSchema]) -> ReversalDataSchema:
        error_msg = f"Para {reversal.type.value}"
        vobo_received = lambda pattern: any(pattern in attach.filename for attach in attachments)
        if reversal.type == ReversalType.porErroresOperativos:
            if not vobo_received("vobo-comercial"):
                raise HTTPException(status_code=400, detail=f"{error_msg} el visto bueno de instancia comercial o jefe de area es obligatorio")
        elif reversal.type == ReversalType.porErroresCliente:
            if not vobo_received("vobo-gte-cuenta"):
                raise HTTPException(status_code=400, detail=f"{error_msg} el visto bueno del gerente de cuenta es obligatorio")
            
            if  is_date_more_than_N_days(reversal.byClient.dateOfIncorrectPayment) and not vobo_received("vobo-riesgos"):
                raise HTTPException(status_code=400, detail=f"{error_msg} el visto bueno de riesgos es obligatorio")
            
                