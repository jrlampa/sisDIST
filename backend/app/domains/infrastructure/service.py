"""Infrastructure domain service."""
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.infrastructure.repository import PoleRepository, ConductorRepository
from app.domains.infrastructure.models import Pole, Conductor
from app.domains.infrastructure.schemas import (
    PoleCreate, PoleUpdate, PoleResponse,
    ConductorCreate, ConductorUpdate, ConductorResponse,
)


class InfrastructureService:
    def __init__(self, db: AsyncSession):
        self.poles = PoleRepository(db)
        self.conductors = ConductorRepository(db)

    # ── Poles ──────────────────────────────────────────────────────────────

    async def list_poles(self, project_id: int | None = None) -> list[PoleResponse]:
        poles = await self.poles.list(project_id)
        return [PoleResponse.model_validate(p) for p in poles]

    async def get_pole(self, pole_id: int) -> PoleResponse | None:
        pole = await self.poles.get(pole_id)
        if pole is None:
            return None
        return PoleResponse.model_validate(pole)

    async def create_pole(self, payload: PoleCreate) -> PoleResponse:
        pole = Pole(**payload.model_dump())
        pole = await self.poles.create(pole)
        return PoleResponse.model_validate(pole)

    async def update_pole(self, pole_id: int, payload: PoleUpdate) -> PoleResponse | None:
        pole = await self.poles.get(pole_id)
        if pole is None:
            return None
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(pole, field, value)
        await self.poles.db.flush()
        await self.poles.db.refresh(pole)
        return PoleResponse.model_validate(pole)

    async def delete_pole(self, pole_id: int) -> bool:
        pole = await self.poles.get(pole_id)
        if pole is None:
            return False
        await self.poles.delete(pole)
        return True

    # ── Conductors ──────────────────────────────────────────────────────────

    async def list_conductors(self, project_id: int | None = None) -> list[ConductorResponse]:
        conductors = await self.conductors.list(project_id)
        return [ConductorResponse.model_validate(c) for c in conductors]

    async def get_conductor(self, conductor_id: int) -> ConductorResponse | None:
        conductor = await self.conductors.get(conductor_id)
        if conductor is None:
            return None
        return ConductorResponse.model_validate(conductor)

    async def create_conductor(self, payload: ConductorCreate) -> ConductorResponse:
        conductor = Conductor(**payload.model_dump())
        conductor = await self.conductors.create(conductor)
        return ConductorResponse.model_validate(conductor)

    async def update_conductor(self, conductor_id: int, payload: ConductorUpdate) -> ConductorResponse | None:
        conductor = await self.conductors.get(conductor_id)
        if conductor is None:
            return None
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(conductor, field, value)
        await self.conductors.db.flush()
        await self.conductors.db.refresh(conductor)
        return ConductorResponse.model_validate(conductor)

    async def delete_conductor(self, conductor_id: int) -> bool:
        conductor = await self.conductors.get(conductor_id)
        if conductor is None:
            return False
        await self.conductors.delete(conductor)
        return True
