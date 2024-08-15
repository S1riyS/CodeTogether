from enum import Enum
from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from models.utils.mixins import IDModelMixin, TimeModelMixin

if TYPE_CHECKING:
    from models import UserModel
    from models.position import PositionModel


class Difficulty(Enum):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'


class ProjectModel(IDModelMixin, TimeModelMixin, Base):
    __tablename__ = "projects"

    name: Mapped[str]
    description: Mapped[str]
    difficulty: Mapped[Difficulty]
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    owner: Mapped["UserModel"] = relationship(back_populates="own_projects")
    positions: Mapped[List["PositionModel"]] = relationship(back_populates='project')

