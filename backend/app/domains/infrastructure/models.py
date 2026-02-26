"""Infrastructure domain DB models — Pole, Conductor, Equipment."""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

try:
    from geoalchemy2 import Geometry as _Geometry
    _POINT = _Geometry("POINT", srid=31983)
except Exception:
    from sqlalchemy import String as _StringFallback
    _POINT = _StringFallback()


def _point_col():
    """Return a geometry Point column, or String when PostGIS is unavailable."""
    try:
        from geoalchemy2 import Geometry
        return Column(Geometry("POINT", srid=31983), nullable=True)
    except Exception:
        return Column(String, nullable=True)


class Pole(Base):
    __tablename__ = "poles"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    code = Column(String(50), nullable=False, index=True)
    location = _point_col()
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    elevation = Column(Float, nullable=True)
    pole_type = Column(String(30), nullable=False, default="concreto")
    pole_height = Column(Float, nullable=True)
    pole_class = Column(String(10), nullable=True)
    owner = Column(String(50), nullable=True)
    observations = Column(Text, nullable=True)
    installed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    conductors_from = relationship("Conductor", foreign_keys="Conductor.pole_from_id", back_populates="pole_from")
    conductors_to = relationship("Conductor", foreign_keys="Conductor.pole_to_id", back_populates="pole_to")
    equipments = relationship("Equipment", back_populates="pole")


class Conductor(Base):
    __tablename__ = "conductors"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    pole_from_id = Column(Integer, ForeignKey("poles.id"), nullable=True)
    pole_to_id = Column(Integer, ForeignKey("poles.id"), nullable=True)
    conductor_type = Column(String(20), nullable=False, default="CA")
    cross_section = Column(Float, nullable=False)
    voltage_level = Column(String(10), nullable=False, default="BT")
    phases = Column(Integer, nullable=False, default=3)
    length = Column(Float, nullable=True)
    observations = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    pole_from = relationship("Pole", foreign_keys=[pole_from_id], back_populates="conductors_from")
    pole_to = relationship("Pole", foreign_keys=[pole_to_id], back_populates="conductors_to")


class Equipment(Base):
    __tablename__ = "equipments"

    id = Column(Integer, primary_key=True, index=True)
    pole_id = Column(Integer, ForeignKey("poles.id"), nullable=False)
    equipment_type = Column(String(50), nullable=False)
    manufacturer = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    observations = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    pole = relationship("Pole", back_populates="equipments")
