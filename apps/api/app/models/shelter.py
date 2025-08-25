from sqlalchemy import Column, String, Boolean, Time, Text, ARRAY, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geography
import uuid
from app.database import Base


class Shelter(Base):
    __tablename__ = "shelters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    lat = Column(NUMERIC(10, 8), nullable=False)
    lon = Column(NUMERIC(11, 8), nullable=False)
    neighborhood = Column(Text, nullable=False)
    phone = Column(Text)
    hours = Column(Text)
    website = Column(Text)
    requires_id = Column(Boolean, default=False)
    pet_friendly = Column(Boolean, default=False)
    ada_accessible = Column(Boolean, default=False)
    lgbtq_friendly = Column(Boolean, default=False)
    curfew_time = Column(Time)
    intake_notes = Column(Text)
    languages = Column(ARRAY(String))

    # Relationships
    statuses = relationship("ShelterStatus", back_populates="shelter", cascade="all, delete-orphan")
    status_changes = relationship("StatusChange", back_populates="shelter", cascade="all, delete-orphan")
    holds = relationship("Hold", back_populates="shelter", cascade="all, delete-orphan")

    # PostGIS geography column for spatial queries
    location = Column(Geography('POINT', srid=4326))

    def __repr__(self):
        return f"<Shelter(id={self.id}, name='{self.name}', neighborhood='{self.neighborhood}')>"


class ShelterStatus(Base):
    __tablename__ = "shelter_status"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shelter_id = Column(UUID(as_uuid=True), ForeignKey("shelters.id"), nullable=False)
    category = Column(
        String,
        CheckConstraint("category IN ('MEN', 'WOMEN', 'FAMILY', 'YOUTH', 'MIXED')"),
        nullable=False
    )
    beds_total = Column(Integer, nullable=False)
    beds_available = Column(Integer, nullable=False)
    status = Column(
        String,
        CheckConstraint("status IN ('OPEN', 'LIMITED', 'FULL', 'UNKNOWN')"),
        nullable=False
    )
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    notes = Column(Text)

    # Relationships
    shelter = relationship("Shelter", back_populates="statuses")

    def __repr__(self):
        return f"<ShelterStatus(shelter_id={self.shelter_id}, category='{self.category}', status='{self.status}')>"
