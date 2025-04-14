from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ProductBase(BaseModel):
    type: str
    
class ProductCreate(ProductBase):
    pvz_id: UUID
    
class ProductResponse(ProductBase):
    id: UUID
    date_time: datetime
    reception_id: UUID