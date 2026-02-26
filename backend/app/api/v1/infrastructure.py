"""Infrastructure API endpoints — poles, conductors, equipment."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.domains.infrastructure.service import InfrastructureService
from app.domains.infrastructure.schemas import (
    PoleCreate, PoleUpdate, PoleResponse,
    ConductorCreate, ConductorUpdate, ConductorResponse,
)

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> InfrastructureService:
    return InfrastructureService(db)


# ── Poles ──────────────────────────────────────────────────────────────────

@router.get("/poles", response_model=list[PoleResponse], summary="Listar postes")
async def list_poles(project_id: int | None = None, service: InfrastructureService = Depends(get_service)):
    return await service.list_poles(project_id)


@router.post("/poles", response_model=PoleResponse, status_code=201, summary="Cadastrar poste")
async def create_pole(payload: PoleCreate, service: InfrastructureService = Depends(get_service)):
    return await service.create_pole(payload)


@router.get("/poles/{pole_id}", response_model=PoleResponse, summary="Obter poste")
async def get_pole(pole_id: int, service: InfrastructureService = Depends(get_service)):
    pole = await service.get_pole(pole_id)
    if not pole:
        raise HTTPException(status_code=404, detail="Poste não encontrado")
    return pole


@router.put("/poles/{pole_id}", response_model=PoleResponse, summary="Atualizar poste")
async def update_pole(pole_id: int, payload: PoleUpdate, service: InfrastructureService = Depends(get_service)):
    pole = await service.update_pole(pole_id, payload)
    if not pole:
        raise HTTPException(status_code=404, detail="Poste não encontrado")
    return pole


@router.delete("/poles/{pole_id}", status_code=204, summary="Remover poste")
async def delete_pole(pole_id: int, service: InfrastructureService = Depends(get_service)):
    deleted = await service.delete_pole(pole_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Poste não encontrado")


# ── Conductors ──────────────────────────────────────────────────────────────

@router.get("/conductors", response_model=list[ConductorResponse], summary="Listar condutores")
async def list_conductors(project_id: int | None = None, service: InfrastructureService = Depends(get_service)):
    return await service.list_conductors(project_id)


@router.post("/conductors", response_model=ConductorResponse, status_code=201, summary="Cadastrar condutor")
async def create_conductor(payload: ConductorCreate, service: InfrastructureService = Depends(get_service)):
    return await service.create_conductor(payload)


@router.get("/conductors/{conductor_id}", response_model=ConductorResponse, summary="Obter condutor")
async def get_conductor(conductor_id: int, service: InfrastructureService = Depends(get_service)):
    conductor = await service.get_conductor(conductor_id)
    if not conductor:
        raise HTTPException(status_code=404, detail="Condutor não encontrado")
    return conductor


@router.put("/conductors/{conductor_id}", response_model=ConductorResponse, summary="Atualizar condutor")
async def update_conductor(
    conductor_id: int, payload: ConductorUpdate, service: InfrastructureService = Depends(get_service)
):
    conductor = await service.update_conductor(conductor_id, payload)
    if not conductor:
        raise HTTPException(status_code=404, detail="Condutor não encontrado")
    return conductor


@router.delete("/conductors/{conductor_id}", status_code=204, summary="Remover condutor")
async def delete_conductor(conductor_id: int, service: InfrastructureService = Depends(get_service)):
    deleted = await service.delete_conductor(conductor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Condutor não encontrado")
