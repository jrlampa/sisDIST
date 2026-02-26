"""Infrastructure domain Pydantic schemas."""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class PoleBase(BaseModel):
    code: str = Field(..., max_length=50, description="Código do poste")
    project_id: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    elevation: Optional[float] = Field(None, description="Altitude em metros")
    pole_type: str = Field("concreto", description="Tipo: concreto, madeira, aço")
    pole_height: Optional[float] = Field(None, description="Altura em metros")
    pole_class: Optional[str] = Field(None, description="Classe conforme NBR")
    owner: Optional[str] = None
    observations: Optional[str] = None


class PoleCreate(PoleBase):
    pass


class PoleUpdate(BaseModel):
    code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    elevation: Optional[float] = None
    pole_type: Optional[str] = None
    pole_height: Optional[float] = None
    pole_class: Optional[str] = None
    owner: Optional[str] = None
    observations: Optional[str] = None


class PoleResponse(PoleBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ConductorBase(BaseModel):
    project_id: Optional[int] = None
    pole_from_id: Optional[int] = None
    pole_to_id: Optional[int] = None
    conductor_type: str = Field("CA", description="Tipo: CA, CAA, ACSR")
    cross_section: float = Field(..., description="Seção transversal em mm²")
    voltage_level: str = Field("BT", description="Nível de tensão: BT ou MT")
    phases: int = Field(3, ge=1, le=3, description="Número de fases")
    length: Optional[float] = Field(None, description="Comprimento em metros")
    observations: Optional[str] = None


class ConductorCreate(ConductorBase):
    pass


class ConductorUpdate(BaseModel):
    conductor_type: Optional[str] = None
    cross_section: Optional[float] = None
    voltage_level: Optional[str] = None
    phases: Optional[int] = None
    length: Optional[float] = None
    observations: Optional[str] = None


class ConductorResponse(ConductorBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
