from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base


class TranslationString(Base):
    __tablename__ = "translation_strings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(Text, nullable=False)
    lang = Column(
        String,
        nullable=False,
        comment="Language code: en, es, ko, hy, tl, zh"
    )
    value = Column(Text, nullable=False)

    def __repr__(self):
        return f"<TranslationString(key='{self.key}', lang='{self.lang}')>"
