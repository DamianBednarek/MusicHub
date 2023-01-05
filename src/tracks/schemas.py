from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel


class BaseTrack(BaseModel):
    id: UUID
    filename: str
    file: str
    track_length: int
    is_public: bool
    created_by: str

    class Config:
        orm_mode = True


class UploadTrack(BaseModel):
    file: UploadFile
    is_public: bool
