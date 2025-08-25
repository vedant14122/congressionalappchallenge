from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base


class Hold(Base):
    __tablename__ = "holds"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shelter_id = Column(UUID(as_uuid=True), ForeignKey("shelters.id"), nullable=False)
    category = Column(
        String,
        CheckConstraint("category IN ('MEN', 'WOMEN', 'FAMILY', 'YOUTH', 'MIXED')"),
        nullable=False
    )
    qty = Column(Integer, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("staff.id"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(
        String,
        CheckConstraint("status IN ('ACTIVE', 'EXPIRED', 'CANCELLED')"),
        nullable=False,
        default="ACTIVE"
    )

    # Relationships
    shelter = relationship("Shelter", back_populates="holds")
    staff = relationship("Staff")

    def __repr__(self):
        return f"<Hold(shelter_id={self.shelter_id}, category='{self.category}', qty={self.qty}, status='{self.status}')>"
