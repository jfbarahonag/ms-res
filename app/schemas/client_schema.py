from pydantic import BaseModel

from app.models.client import DocumentType

class ClientSchema(BaseModel):
    name: str
    document_type: DocumentType
    document_number: str
    email: str