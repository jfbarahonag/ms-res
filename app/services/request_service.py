from app.schemas.request_schema import RequestMaintenanceSchema, RequestDraftMaintenanceSchema
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

redirect_draft = {
    MaintenanceType.REVERSAL: lambda x: RequestReversalService.handle_draft_reversal_request(x),
    MaintenanceType.TYPE_2: lambda x: f"2 Hola {x}",
    MaintenanceType.TYPE_3: lambda x: f"3 Hola {x}",
    MaintenanceType.TYPE_4: lambda x: f"4 Hola {x}",
    MaintenanceType.TYPE_5: lambda x: f"5 Hola {x}",
    MaintenanceType.TYPE_OTHER: lambda x: f"6 Hola {x}",
}

redirect_query = {
    MaintenanceType.REVERSAL: lambda id: RequestReversalService.get_reversal(id),
    MaintenanceType.TYPE_2: lambda id: f"2 Hola {id}",
    MaintenanceType.TYPE_3: lambda id: f"3 Hola {id}",
    MaintenanceType.TYPE_4: lambda id: f"4 Hola {id}",
    MaintenanceType.TYPE_5: lambda id: f"5 Hola {id}",
    MaintenanceType.TYPE_OTHER: lambda id: f"6 Hola {id}",
}

class RequestService:
    @staticmethod
    def handle_draft_maintenance_request(request: RequestDraftMaintenanceSchema):
        return redirect_draft[request.maintenance.type](request)
    
    @staticmethod
    def handle_maintenance_request(request: RequestMaintenanceSchema):
        return redirect_request[request.maintenance.type](request)
    
    @staticmethod
    def get_maintenance_info(maintenance_id: int, type: MaintenanceType):
        return redirect_query[type](maintenance_id)
