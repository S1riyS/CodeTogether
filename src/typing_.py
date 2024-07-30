from typing import TypeVar, TypeAlias
from uuid import UUID

from pydantic import BaseModel

from core.database import Base

IDType: TypeAlias = UUID
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
