from sqlalchemy import Column, String, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, CITEXT
from sqlalchemy.orm import relationship
import uuid
from app.database import Base


class Staff(Base):
    __tablename__ = "staff"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(CITEXT, unique=True, nullable=False)
    shelter_id = Column(UUID(as_uuid=True), ForeignKey("shelters.id"), nullable=True)
    role = Column(
        String,
        CheckConstraint("role IN ('ADMIN', 'STAFF')"),
        nullable=False,
        default="STAFF"
    )
    locale = Column(String, default="en")

    # Relationships
    shelter = relationship("Shelter")

    def __repr__(self):
        return f"<Staff(id={self.id}, email='{self.email}', role='{self.role}')>"
