from fastapi import APIRouter

from app.services.res_service import RESService

router = APIRouter(prefix="/res")

@router.get("")
def hello_world():
    return RESService.hello_world()