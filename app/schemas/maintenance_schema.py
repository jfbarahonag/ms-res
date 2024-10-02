from pydantic import BaseModel
from typing import Optional

from app.models.maintenance import MaintenanceType, MaintenanceInfoType
from app.models.reversal import ReversalType
from app.schemas.common_schema import AttachmentsSchema

class MaintenanceInfoSchema(BaseModel):
    key: str
    value: str
    type: MaintenanceInfoType

class DraftMaintenanceSchema(BaseModel):
    type: MaintenanceType

class MaintenanceSchema(DraftMaintenanceSchema):
    subType: Optional[ReversalType] = "N/A" # Lista de subtipos
    attachments: Optional[list[AttachmentsSchema]] = None
    info: list[MaintenanceInfoSchema]