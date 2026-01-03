from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum




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