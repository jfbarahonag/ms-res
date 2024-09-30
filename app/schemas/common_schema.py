from pydantic import BaseModel
from typing import Optional

class AttachmentsSchema(BaseModel):
    filename: str
    content: str
    comment: Optional[str] = "Sin comentario"