from datetime import datetime, timedelta
from fastapi import HTTPException

from app.schemas.request_schema import RequestMaintenanceSchema, RequestDraftMaintenanceSchema
from app.schemas.maintenance_schema import MaintenanceSchema, AttachmentsSchema
from app.schemas.reversal_schema import ReversalDataSchema

from app.models.reversal import ReversalType

from app.services.motor_service import MotorService
from app.services.attachments_service import AttachmentsService

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
        data_copy = data.model_dump().copy()
        motor_payload = {}
        
        motor_payload["advisor"] = data_copy["advisor"]
        motor_payload["client"] = data_copy["client"]
        response = MotorService.create_draft(motor_payload)
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
        
        valid_sub_types = ['Reversion por errores operativos','Reversion por errores del cliente']
        if maintenance.subType not in valid_sub_types:
            raise HTTPException(status_code=400, detail=f"'{maintenance.subType}' no es una reversion valida")  
            
        if maintenance.subType == "N/A":
            raise HTTPException(status_code=400, detail="Debe seleccionarse un tipo de reversion")  
        
        reversal_fields = ["dateOfIncorrectPayment", "errors", "correctiveActions"]
        is_valid_data = any(i for i in maintenance.info if i.key in reversal_fields)
        
        if not is_valid_data:
            raise HTTPException(status_code=400, detail="No hay items validos")  
        
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
            
    @staticmethod
    def get_reversal(reversal_id: int):
        return MotorService.get(reversal_id)
    
    @staticmethod
    def send_files(reversal_id:int, file_paths: list):
        try:
            
            # Preparar los archivos para enviarlos como multipart/form-data
            files, files_opened = AttachmentsService.filepaths_to_multipart(file_paths)
            response = MotorService.attach_files(reversal_id, files)
            AttachmentsService.close_open_files(files_opened)
            
            return response
        
        except Exception as e:
            print(f"Error al enviar los archivos: {str(e)}")
            raise e
        
        finally:
            # Eliminar los archivos después de intentar enviarlos, exitoso o no
            AttachmentsService.delete_files(file_paths)

    @staticmethod
    def handle_update_reversal(reversal_id: int, data: MaintenanceSchema):
        
        reversal = RequestReversalService.parse_as_reversal(data)
        
        RequestReversalService.validate_mandatory_attachments(reversal, data.attachments)
        
        file_paths = []
        for attachment in data.attachments:
            file_path = AttachmentsService.b64_to_file(attachment.content, attachment.filename)
            file_paths.append(file_path)
        
        return RequestReversalService.send_files(reversal_id, file_paths)