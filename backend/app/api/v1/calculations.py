"""Calculations API endpoints — voltage drop, mechanical stress, material list."""
from fastapi import APIRouter, HTTPException
from app.domains.calculations.schemas import (
    VoltageDropRequest, VoltageDropResponse,
    MechanicalStressRequest, MechanicalStressResponse,
    MaterialListRequest, MaterialListResponse,
)
from app.domains.calculations.voltage_drop import calculate_voltage_drop
from app.domains.calculations.mechanical_stress import calculate_mechanical_stress

router = APIRouter()


@router.post("/voltage-drop", response_model=VoltageDropResponse, summary="Calcular queda de tensão (NBR 5410)")
async def voltage_drop(payload: VoltageDropRequest):
    """Calcula queda de tensão conforme ABNT NBR 5410."""
    try:
        return calculate_voltage_drop(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post(
    "/mechanical-stress",
    response_model=MechanicalStressResponse,
    summary="Calcular esforço mecânico em postes (NBR 8458/8798)",
)
async def mechanical_stress(payload: MechanicalStressRequest):
    """Calcula esforço mecânico em postes conforme ABNT NBR 8458/8798."""
    try:
        return calculate_mechanical_stress(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/material-list", response_model=MaterialListResponse, summary="Gerar lista de material")
async def material_list(payload: MaterialListRequest):
    """Gera lista de material para rede de distribuição aérea."""
    items = []
    for item in payload.items:
        items.append({
            "codigo": item.codigo,
            "descricao": item.descricao,
            "unidade": item.unidade,
            "quantidade": item.quantidade,
        })
    return MaterialListResponse(
        projeto=payload.projeto,
        concessionaire=payload.concessionaire,
        items=items,
        total_items=len(items),
    )
