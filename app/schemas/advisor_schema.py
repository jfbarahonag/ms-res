from pydantic import BaseModel

class AdvisorSchema(BaseModel):
    name: str
    email: str