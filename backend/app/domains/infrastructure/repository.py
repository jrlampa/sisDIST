"""Infrastructure domain repository."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domains.infrastructure.models import Pole, Conductor


class PoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self, project_id: int | None = None) -> list[Pole]:
        q = select(Pole)
        if project_id is not None:
            q = q.where(Pole.project_id == project_id)
        result = await self.db.execute(q)
        return list(result.scalars().all())

    async def get(self, pole_id: int) -> Pole | None:
        result = await self.db.execute(select(Pole).where(Pole.id == pole_id))
        return result.scalar_one_or_none()

    async def create(self, pole: Pole) -> Pole:
        self.db.add(pole)
        await self.db.flush()
        await self.db.refresh(pole)
        return pole

    async def delete(self, pole: Pole) -> None:
        await self.db.delete(pole)
        await self.db.flush()


class ConductorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self, project_id: int | None = None) -> list[Conductor]:
        q = select(Conductor)
        if project_id is not None:
            q = q.where(Conductor.project_id == project_id)
        result = await self.db.execute(q)
        return list(result.scalars().all())

    async def get(self, conductor_id: int) -> Conductor | None:
        result = await self.db.execute(select(Conductor).where(Conductor.id == conductor_id))
        return result.scalar_one_or_none()

    async def create(self, conductor: Conductor) -> Conductor:
        self.db.add(conductor)
        await self.db.flush()
        await self.db.refresh(conductor)
        return conductor

    async def delete(self, conductor: Conductor) -> None:
        await self.db.delete(conductor)
        await self.db.flush()
