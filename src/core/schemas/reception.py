from pydantic import BaseModel
from typing import List
from uuid import UUID
from datetime import datetime
from core.schemas.product import ProductResponse

class ReceptionBase(BaseModel):
    pvz_id: UUID
    
class ReceptionCreate(ReceptionBase):
    pass
    
class ReceptionResponse(ReceptionBase):
    id: UUID
    date_time: datetime
    status: str
    
class ReceptionWithProducts(ReceptionResponse):
    products: List[ProductResponse]