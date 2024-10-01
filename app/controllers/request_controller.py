from fastapi import APIRouter

from app.services.request_service import RequestService
from app.schemas.request_schema import RequestMaintenanceSchema

router = APIRouter(prefix="/res")

@router.post("/request")
def handle_request_reception(request_data: RequestMaintenanceSchema):
    return RequestService.handle_maintenance_request(request_data.maintenance)