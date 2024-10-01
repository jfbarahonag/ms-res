from pydantic import BaseModel
from typing import Optional

from app.schemas.client_schema import ClientSchema
from app.schemas.advisor_schema import AdvisorSchema
from app.schemas.maintenance_schema import MaintenanceSchema

class RequestSchema(BaseModel):
    client: ClientSchema
    advisor: AdvisorSchema
    maintenance: MaintenanceSchema