from pydantic import BaseModel


class DeleteResponseSchema(BaseModel):
    success: bool
