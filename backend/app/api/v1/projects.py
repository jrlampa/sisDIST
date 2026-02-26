"""Projects API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.domains.projects.service import ProjectService
from app.domains.projects.schemas import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> ProjectService:
    return ProjectService(db)


@router.get("/", response_model=list[ProjectResponse], summary="Listar projetos")
async def list_projects(service: ProjectService = Depends(get_service)):
    return await service.list_projects()


@router.post("/", response_model=ProjectResponse, status_code=201, summary="Criar projeto")
async def create_project(payload: ProjectCreate, service: ProjectService = Depends(get_service)):
    return await service.create_project(payload)


@router.get("/{project_id}", response_model=ProjectResponse, summary="Obter projeto")
async def get_project(project_id: int, service: ProjectService = Depends(get_service)):
    project = await service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return project


@router.put("/{project_id}", response_model=ProjectResponse, summary="Atualizar projeto")
async def update_project(
    project_id: int, payload: ProjectUpdate, service: ProjectService = Depends(get_service)
):
    project = await service.update_project(project_id, payload)
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return project


@router.delete("/{project_id}", status_code=204, summary="Remover projeto")
async def delete_project(project_id: int, service: ProjectService = Depends(get_service)):
    deleted = await service.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")


@router.get("/{project_id}/material-list", summary="Gerar lista de material do projeto")
async def project_material_list(project_id: int, service: ProjectService = Depends(get_service)):
    material_list = await service.generate_material_list(project_id)
    if material_list is None:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return material_list
