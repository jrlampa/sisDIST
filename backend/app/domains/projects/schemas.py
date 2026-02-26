"""Projects domain Pydantic schemas."""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class ProjectBase(BaseModel):
    name: str = Field(..., max_length=200, description="Nome do projeto")
    description: Optional[str] = None
    concessionaire: str = Field("Enel-RJ", description="Concessionária: Enel-RJ ou Light")
    area_wkt: Optional[str] = Field(None, description="Polígono da área em WKT")


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    concessionaire: Optional[str] = None
    area_wkt: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
