from pydantic import BaseModel
from typing import Optional

class OperationRecord(BaseModel):
    id: int
    operation_id: int
    user_id: int
    amount: str
    user_balance: float
    operation_response: str
    date: str
    deleted_at: Optional[str]
    type:str