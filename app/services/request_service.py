from app.config.variables import URL_MOTOR

from app.schemas.maintenance_schema import MaintenanceSchema
from app.models.maintenance import MaintenanceType

from app.services.reversal_service import RequestReversalService

redirect_request = {
    MaintenanceType.REVERSAL: lambda x: RequestReversalService.handle_reversal_request(x),
    MaintenanceType.TYPE_2: lambda x: f"2 Hola {x}",
    MaintenanceType.TYPE_3: lambda x: f"3 Hola {x}",
    MaintenanceType.TYPE_4: lambda x: f"4 Hola {x}",
    MaintenanceType.TYPE_5: lambda x: f"5 Hola {x}",
    MaintenanceType.TYPE_OTHER: lambda x: f"6 Hola {x}",
}

class RequestService:
    @staticmethod
    def handle_maintenance_request(maintenance: MaintenanceSchema):
        return redirect_request[maintenance.type](maintenance)
    
    @staticmethod
    def get_request(request_id: int):
        return URL_MOTOR
    
    @staticmethod
    def hello_world():
        return "Hello world"