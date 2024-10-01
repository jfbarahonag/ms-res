from pydantic import BaseModel
from typing import Optional

from app.models.client import UserDocumentType

class ClientSchema(BaseModel):
    companyName: str
    NIT: str
    obligationNumber: str
    username: str
    userDocumentType: UserDocumentType
    userDocumentNumber: str
    userEmail: str
    phone: Optional[str]