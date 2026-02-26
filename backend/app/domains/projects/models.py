"""Projects domain DB models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    concessionaire = Column(String(50), nullable=False, default="Enel-RJ")
    area_wkt = Column(Text, nullable=True)  # WKT polygon string
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
