from fastapi import APIRouter

from app.services.request_service import RequestService

router = APIRouter(prefix="/res")

@router.get("")
def hello_world():
    return RequestService.hello_world()

@router.post("/request")
def handle_request_reception():
    return RequestService.hello_world()