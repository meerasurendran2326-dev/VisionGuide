from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.location import LocationCreate, LocationOut
from app.services.firestore_service import FirestoreService

router = APIRouter(prefix="/location", tags=["Location"])


def get_firestore_service() -> FirestoreService:
    """Dependency provider for the Firestore service."""
    return FirestoreService()


@router.post(
    "",
    response_model=LocationOut,
    status_code=status.HTTP_201_CREATED,
    summary="Store a user's latest location",
    description="Persist a location update for a user in Firestore.",
)
def save_location(
    payload: LocationCreate,
    service: Annotated[FirestoreService, Depends(get_firestore_service)],
) -> LocationOut:
    """Store a new location update and return the saved record."""
    try:
        saved_location = service.update_location(
            payload.userId,
            payload.latitude,
            payload.longitude,
        )
        return LocationOut(**saved_location)
    except HTTPException:
        raise
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get(
    "/{user_id}",
    response_model=LocationOut,
    status_code=status.HTTP_200_OK,
    summary="Fetch the latest saved location",
    description="Return the most recent location stored for the provided user ID.",
)
def get_location(
    user_id: str,
    service: Annotated[FirestoreService, Depends(get_firestore_service)],
) -> LocationOut:
    """Return the latest stored location for a user, if it exists."""
    try:
        latest_location = service.get_latest_location(user_id)
        if latest_location is None:
            raise HTTPException(status_code=404, detail="Location not found for the provided user")
        return LocationOut(**latest_location)
    except HTTPException:
        raise
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail=str(exc)) from exc
