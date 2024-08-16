from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from models.utils.mixins import TimeModelMixin

if TYPE_CHECKING:
    from models import UserModel, PositionModel


class ApplicationModel(Base, TimeModelMixin):
    __tablename__ = 'applications'
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "position_id",
            name="idx_unique_user_position",
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    position_id: Mapped[UUID] = mapped_column(ForeignKey('positions.id'))
    message: Mapped[str]
    is_approved: Mapped[bool] = mapped_column(default=False)

    # Association between Association -> User
    user: Mapped["UserModel"] = relationship(back_populates="positions_details")
    # Association between Association -> Position
    position: Mapped["PositionModel"] = relationship(back_populates="users_details")
