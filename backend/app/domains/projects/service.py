"""Projects domain service."""
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.projects.repository import ProjectRepository
from app.domains.projects.models import Project
from app.domains.projects.schemas import ProjectCreate, ProjectUpdate, ProjectResponse


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.repo = ProjectRepository(db)

    async def list_projects(self) -> list[ProjectResponse]:
        projects = await self.repo.list()
        return [ProjectResponse.model_validate(p) for p in projects]

    async def get_project(self, project_id: int) -> ProjectResponse | None:
        project = await self.repo.get(project_id)
        if project is None:
            return None
        return ProjectResponse.model_validate(project)

    async def create_project(self, payload: ProjectCreate) -> ProjectResponse:
        project = Project(**payload.model_dump())
        project = await self.repo.create(project)
        return ProjectResponse.model_validate(project)

    async def update_project(self, project_id: int, payload: ProjectUpdate) -> ProjectResponse | None:
        project = await self.repo.get(project_id)
        if project is None:
            return None
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(project, field, value)
        project.updated_at = datetime.utcnow()
        await self.repo.db.flush()
        await self.repo.db.refresh(project)
        return ProjectResponse.model_validate(project)

    async def delete_project(self, project_id: int) -> bool:
        project = await self.repo.get(project_id)
        if project is None:
            return False
        await self.repo.delete(project)
        return True

    async def generate_material_list(self, project_id: int) -> dict | None:
        project = await self.repo.get(project_id)
        if project is None:
            return None
        # Placeholder: in production, query poles/conductors/equipment for this project
        return {
            "projeto_id": project_id,
            "projeto_nome": project.name,
            "concessionaire": project.concessionaire,
            "items": [],
            "observacao": "Lista de material gerada automaticamente pelo sisDIST",
        }
