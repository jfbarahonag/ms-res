from pydantic import BaseModel
from typing import Optional

from app.models.maintenance import MaintenanceType, MaintenanceInfoType
from app.schemas.common_schema import AttachmentsSchema

class MaintenanceInfoSchema(BaseModel):
    key: str
    value: str
    type: MaintenanceInfoType

class MaintenanceSchema(BaseModel):
    type: MaintenanceType
    subType: str
    attachments: Optional[list[AttachmentsSchema]] = None
    info: list[MaintenanceInfoSchema]