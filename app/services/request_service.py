from app.config.variables import URL_MOTOR

from app.schemas.maintenance_schema import MaintenanceSchema
from app.models.maintenance import MaintenanceType

redirect_request = {
    MaintenanceType.TYPE_1: lambda x: f"1 Hola {x}",
    MaintenanceType.TYPE_2: lambda x: f"2 Hola {x}",
    MaintenanceType.TYPE_3: lambda x: f"3 Hola {x}",
    MaintenanceType.TYPE_4: lambda x: f"4 Hola {x}",
    MaintenanceType.TYPE_5: lambda x: f"5 Hola {x}",
    MaintenanceType.TYPE_OTHER: lambda x: f"6 Hola {x}",
}

class RequestService:
    
    
    @staticmethod
    def handle_maintenance_request(maintenance: MaintenanceSchema):
        return redirect_request[maintenance.type](maintenance.subType)
    
    @staticmethod
    def get_request(request_id: int):
        return URL_MOTOR
    
    @staticmethod
    def hello_world():
        return "Hello world"