from fastapi import APIRouter

from app.services.request_service import RequestService
from app.schemas.request_schema import RequestSchema

router = APIRouter(prefix="/res")

@router.get("")
def hello_world():
    return RequestService.hello_world()

@router.post("/request")
def handle_request_reception(request_data: RequestSchema):
    print(request_data)
    return RequestService.hello_world()