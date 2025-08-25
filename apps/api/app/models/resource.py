from sqlalchemy import Column, String, Text, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from geoalchemy2 import Geography
import uuid
from app.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    type = Column(
        String,
        CheckConstraint(
            "type IN ('FOOD', 'SHOWER', 'HEALTH', 'LEGAL', 'EMPLOYMENT', 'HYGIENE', 'COOLING', 'WARMING', 'SAFE_PARKING')"
        ),
        nullable=False
    )
    address = Column(Text, nullable=False)
    lat = Column(NUMERIC(10, 8), nullable=False)
    lon = Column(NUMERIC(11, 8), nullable=False)
    neighborhood = Column(Text, nullable=False)
    hours = Column(Text)
    phone = Column(Text)
    notes = Column(Text)

    # PostGIS geography column for spatial queries
    location = Column(Geography('POINT', srid=4326))

    def __repr__(self):
        return f"<Resource(id={self.id}, name='{self.name}', type='{self.type}', neighborhood='{self.neighborhood}')>"
