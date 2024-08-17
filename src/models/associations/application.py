from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from models.utils.mixins import TimeModelMixin

if TYPE_CHECKING:
    from models import UserModel, PositionModel


class ApplicationStatus(Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'


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
    status: Mapped[ApplicationStatus] = mapped_column(
        default=ApplicationStatus.PENDING.value,
        server_default=ApplicationStatus.PENDING.value
    )

    # Association between Association -> User
    user: Mapped["UserModel"] = relationship(back_populates="positions_details")
    # Association between Association -> Position
    position: Mapped["PositionModel"] = relationship(back_populates="users_details")
