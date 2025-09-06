from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import TimestampMixin


class Note(TimestampMixin, Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    content: Mapped[str | None]
    is_archived: Mapped[bool] = mapped_column(Boolean, server_default="false")

    tags = relationship(
        "Tag",
        secondary="note_tags",
        back_populates="notes",
        lazy="selectin",
        passive_deletes=True,
    )
