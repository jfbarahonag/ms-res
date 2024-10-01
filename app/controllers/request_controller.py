from fastapi import APIRouter

from app.services.request_service import RequestService
from app.schemas.request_schema import RequestSchema

router = APIRouter(prefix="/res")

@router.post("/request")
def handle_request_reception(request_data: RequestSchema):
    return RequestService.handle_maintenance_request(request_data.maintenance)