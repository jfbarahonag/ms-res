from fastapi import APIRouter

from app.models.maintenance import MaintenanceType

from app.services.request_service import RequestService
from app.schemas.request_schema import RequestMaintenanceSchema, RequestDraftMaintenanceSchema, MaintenanceSchema

router = APIRouter(prefix="/res")

@router.post("/request")
def handle_request_reception(request_data: RequestMaintenanceSchema):
    return RequestService.handle_maintenance_request(request_data)

@router.post("/request/draft")
def handle_draft_reception(request_data: RequestDraftMaintenanceSchema):
    return RequestService.handle_draft_maintenance_request(request_data)

@router.get("/request/{maintenance_id}")
def get_draft_info(maintenance_id: int, type: MaintenanceType):
    return RequestService.get_maintenance_info(maintenance_id, type)

@router.put("/request/draft/{maintenance_id}")
def update_maintenance_info(maintenance_id:int, data:MaintenanceSchema):
    return RequestService.handle_maintenance_update(maintenance_id, data)