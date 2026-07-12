from pydantic import BaseModel, Field


class LocationCreate(BaseModel):
    userId: str = Field(..., min_length=1)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class LocationOut(BaseModel):
    userId: str
    latitude: float
    longitude: float
    updatedAt: str
