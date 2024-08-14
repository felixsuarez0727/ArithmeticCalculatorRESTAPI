from pydantic import BaseModel

class Operation(BaseModel):
    num_a: float
    num_b: float
    operation: str