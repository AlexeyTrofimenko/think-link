from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import TimestampMixin
from .note_tag import note_tags

if TYPE_CHECKING:
    from .tag import Tag


class Note(TimestampMixin, Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    content: Mapped[str | None]
    is_archived: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))

    tags: Mapped[list[Tag]] = relationship(
        secondary=note_tags,
        back_populates="notes",
        lazy="selectin",
        passive_deletes=True,
    )
