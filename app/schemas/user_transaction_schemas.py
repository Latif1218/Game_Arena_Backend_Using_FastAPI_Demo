from pydantic import BaseModel
from typing import Optional
from datetime import datetime





class TransactionOut(BaseModel):
    id: int
    amount: float
    type: str
    status: str
    transaction_id: str
    description: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True
        use_enum_values = True