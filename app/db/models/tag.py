from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.note import Note

from .base import Base
from .mixins import TimestampMixin
from .note_tag import note_tags

if TYPE_CHECKING:
    from .note import Note


class Tag(TimestampMixin, Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    notes: Mapped[list[Note]] = relationship(
        secondary=note_tags,
        back_populates="tags",
        lazy="selectin",
        passive_deletes=True,
    )
