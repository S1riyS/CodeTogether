from typing import TYPE_CHECKING, Optional, List
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from models.utils.mixins import IDModelMixin

if TYPE_CHECKING:
    from models import ProjectModel
    from models.associations import ApplicationModel


class PositionModel(Base, IDModelMixin):
    __tablename__ = "positions"

    name: Mapped[str]
    description: Mapped[Optional[str]]
    count: Mapped[int] = mapped_column(default=1)
    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))

    project: Mapped["ProjectModel"] = relationship(back_populates="positions")
    users_details: Mapped[List["ApplicationModel"]] = relationship(back_populates="position")
