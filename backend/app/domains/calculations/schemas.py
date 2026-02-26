"""Calculations domain Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import Optional, Literal


# ── Conductor data ──────────────────────────────────────────────────────────

class ConductorProperties(BaseModel):
    conductor_type: str
    cross_section: float
    resistance: float = Field(..., description="Resistência em Ω/km")
    reactance: float = Field(..., description="Reatância em Ω/km")


# ── Voltage Drop ────────────────────────────────────────────────────────────

class VoltageDropRequest(BaseModel):
    current: float = Field(..., gt=0, description="Corrente em Amperes")
    length: float = Field(..., gt=0, description="Comprimento do trecho em metros")
    conductor_type: str = Field("CA", description="Tipo de condutor: CA, CAA, ACSR")
    cross_section: float = Field(..., gt=0, description="Seção transversal em mm²")
    power_factor: float = Field(0.92, ge=0.0, le=1.0, description="Fator de potência (cosφ)")
    phases: Literal[1, 3] = Field(3, description="Número de fases: 1 ou 3")
    nominal_voltage: float = Field(220.0, gt=0, description="Tensão nominal em Volts")
    voltage_level: str = Field("BT", description="Nível de tensão: BT ou MT")


class VoltageDropResponse(BaseModel):
    voltage_drop_v: float = Field(..., description="Queda de tensão absoluta em Volts")
    voltage_drop_pct: float = Field(..., description="Queda de tensão percentual (%)")
    limit_pct: float = Field(..., description="Limite regulatório (%)")
    compliant: bool = Field(..., description="Atende ao limite normativo?")
    resistance: float = Field(..., description="Resistência do condutor em Ω/km")
    reactance: float = Field(..., description="Reatância do condutor em Ω/km")
    standard: str = "ABNT NBR 5410"


# ── Mechanical Stress ───────────────────────────────────────────────────────

class MechanicalStressRequest(BaseModel):
    wind_speed: float = Field(..., gt=0, description="Velocidade do vento em m/s")
    conductor_diameter: float = Field(..., gt=0, description="Diâmetro do condutor em mm")
    span_length: float = Field(..., gt=0, description="Vão em metros")
    conductor_weight: float = Field(..., gt=0, description="Peso do condutor em kg/km")
    conductor_tension: float = Field(..., gt=0, description="Tensão mecânica no condutor em N")
    pole_height: float = Field(11.0, gt=0, description="Altura do poste em metros")
    attachment_height: float = Field(10.0, gt=0, description="Altura do ponto de fixação em metros")
    num_conductors: int = Field(3, ge=1, le=6, description="Número de condutores no cruzeta")


class MechanicalStressResponse(BaseModel):
    wind_load_per_conductor_n: float = Field(..., description="Carga de vento por condutor em N")
    weight_load_per_conductor_n: float = Field(..., description="Carga de peso por condutor em N")
    tension_load_n: float = Field(..., description="Carga de tração no poste em N")
    total_resultant_n: float = Field(..., description="Resultante total no poste em N")
    moment_nm: float = Field(..., description="Momento fletor no engastamento em N·m")
    safety_factor_required: float = 2.5
    standard: str = "ABNT NBR 8458/8798"


# ── Material List ───────────────────────────────────────────────────────────

class MaterialItem(BaseModel):
    codigo: str
    descricao: str
    unidade: str
    quantidade: float


class MaterialListRequest(BaseModel):
    projeto: str
    concessionaire: str = Field("Enel-RJ", description="Concessionária: Enel-RJ ou Light")
    items: list[MaterialItem] = []


class MaterialListResponse(BaseModel):
    projeto: str
    concessionaire: str
    items: list[dict]
    total_items: int
