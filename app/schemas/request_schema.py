from pydantic import BaseModel
from typing import Optional

from app.schemas.client_schema import ClientSchema
from app.schemas.advisor_schema import AdvisorSchema
from app.models.maintenance import MaintenanceType

class AttachmentSchema(BaseModel):
    filename: str
    content: str
    comment: Optional[str] = "Sin comentario"

class RequestData(BaseModel):
    request_type: MaintenanceType
    sub_request_type: MaintenanceType
    attachments: Optional[list[AttachmentSchema]] = []

class RequestSchema(BaseModel):
    client: ClientSchema
    advisor: AdvisorSchema
    data: RequestData