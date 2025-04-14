from pydantic import BaseModel
from typing import List
from uuid import UUID
from datetime import datetime
from core.schemas.reception import ReceptionWithProducts

class PVZBase(BaseModel):
    city: str
    
class PVZCreate(PVZBase):
    pass
    
class PVZResponse(PVZBase):
    id: UUID
    registration_date: datetime
    
class PVZWithReceptions(PVZResponse):
    receptions: List[ReceptionWithProducts]