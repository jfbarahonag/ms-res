from pydantic import BaseModel
from typing import Optional

from app.models.client import CompanyDocumentType, UserDocumentType

class UserSchema(BaseModel):
    name: str
    document_type: UserDocumentType
    document_number: str
    email: str
    phone: Optional[str] = None
    

class ClientSchema(BaseModel):
    name: str
    document_type: CompanyDocumentType
    document_number: str
    user: UserSchema