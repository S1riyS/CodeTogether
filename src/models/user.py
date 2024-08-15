from typing import TYPE_CHECKING, List

from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.database import Base
from models.utils.mixins import IDModelMixin, TimeModelMixin

if TYPE_CHECKING:
    from models import ProjectModel
    from models.associations import UserPositionAssociation


class UserModel(IDModelMixin, TimeModelMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    avatar_url: Mapped[str] = mapped_column(nullable=True)
    is_verified: Mapped[bool] = mapped_column(default=False)

    own_projects: Mapped[List["ProjectModel"]] = relationship(back_populates="owner")
    positions_details: Mapped[List["UserPositionAssociation"]] = relationship(back_populates="user")
