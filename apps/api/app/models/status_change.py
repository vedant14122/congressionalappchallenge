from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base


class StatusChange(Base):
    __tablename__ = "status_changes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shelter_id = Column(UUID(as_uuid=True), ForeignKey("shelters.id"), nullable=False)
    category = Column(
        String,
        CheckConstraint("category IN ('MEN', 'WOMEN', 'FAMILY', 'YOUTH', 'MIXED')"),
        nullable=False
    )
    prev_available = Column(Integer, nullable=False)
    new_available = Column(Integer, nullable=False)
    changed_by = Column(UUID(as_uuid=True), ForeignKey("staff.id"), nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    shelter = relationship("Shelter", back_populates="status_changes")
    staff = relationship("Staff")

    def __repr__(self):
        return f"<StatusChange(shelter_id={self.shelter_id}, category='{self.category}', prev={self.prev_available}, new={self.new_available})>"
