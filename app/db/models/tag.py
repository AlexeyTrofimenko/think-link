from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .mixins import TimestampMixin

class Tag(TimestampMixin, Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    notes = relationship(
        "Note",
        secondary="note_tags",
        back_populates="tags",
        lazy="selectin",
        passive_deletes=True,
    )
