from datetime import datetime
from uuid import UUID


class IDSchemaMixin:
    id: UUID


class TimeSchemaMixin:
    created_at: datetime
    updated_at: datetime