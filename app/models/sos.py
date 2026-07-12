from pydantic import BaseModel, Field


class SOSCreate(BaseModel):
    userId: str = Field(..., min_length=1)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class SOSOut(BaseModel):
    message: str
