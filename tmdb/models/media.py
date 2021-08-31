from pydantic import BaseModel


class MediaRequestObject(BaseModel):
    media_type: str
    media_id: int
    favorite: bool
