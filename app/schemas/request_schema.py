from pydantic import BaseModel

from app.schemas.client_schema import ClientSchema

class RequestSchema(BaseModel):
    client: ClientSchema
    commercial_adviser_email: str
    title: str
    description: str