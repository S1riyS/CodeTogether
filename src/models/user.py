from sqlalchemy.orm import mapped_column, Mapped

from core.database import Base
from .utils.mixins import IDModelMixin, TimeModelMixin


class UserModel(IDModelMixin, TimeModelMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    username: Mapped[str]
    avatar_url: Mapped[str] = mapped_column(nullable=True, default=True)
    is_verified: Mapped[bool] = mapped_column(default=True)
