from pydantic import BaseModel
from typing import Optional

from app.models.reversal import ReversalType

class ReversalByOperational(BaseModel):
    errors: str
    correctiveActions: str

class ReversalByClient(BaseModel):
    dateOfIncorrectPayment: str

class ReversalDataSchema(BaseModel):
    type: ReversalType
    byOperational: Optional[ReversalByOperational] = None
    byClient: Optional[ReversalByClient] = None