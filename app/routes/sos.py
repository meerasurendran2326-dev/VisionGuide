from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.sos import SOSCreate, SOSOut
from app.services.firestore_service import FirestoreService

router = APIRouter(prefix="/sos", tags=["SOS"])


def get_firestore_service() -> FirestoreService:
    """Dependency provider for the Firestore service."""
    return FirestoreService()


@router.post(
    "",
    response_model=SOSOut,
    status_code=status.HTTP_201_CREATED,
    summary="Send an SOS alert",
    description="Store an emergency alert with the user's location and status in Firestore.",
)
def send_sos(
    payload: SOSCreate,
    service: Annotated[FirestoreService, Depends(get_firestore_service)],
) -> SOSOut:
    """Persist an SOS request and return a confirmation message."""
    try:
        service.create_sos(payload.userId, payload.latitude, payload.longitude)
        return SOSOut(message="SOS Sent Successfully")
    except HTTPException:
        raise
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail=str(exc)) from exc
