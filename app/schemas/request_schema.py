from pydantic import BaseModel
from typing import Optional

from app.schemas.client_schema import ClientSchema
from app.schemas.advisor_schema import AdvisorSchema
from app.schemas.maintenance_schema import MaintenanceSchema, DraftMaintenanceSchema

class RequestMaintenanceMandatory(BaseModel):
    client: ClientSchema
    advisor: AdvisorSchema

class RequestMaintenanceSchema(RequestMaintenanceMandatory):
    maintenance: MaintenanceSchema

class RequestDraftMaintenanceSchema(RequestMaintenanceMandatory):
    maintenance: DraftMaintenanceSchema