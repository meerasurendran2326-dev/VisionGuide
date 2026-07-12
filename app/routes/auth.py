from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models.user import UserCreate, UserLogin, UserOut
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()
security = HTTPBearer(auto_error=False)


def get_auth_service() -> AuthService:
    """Dependency provider for the authentication service."""
    return auth_service


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new Firebase Authentication user and save their profile in Firestore.",
)
def register_user(
    payload: UserCreate,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserOut:
    """Register a new user and return the created profile."""
    try:
        return service.register(payload)
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post(
    "/login",
    response_model=dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Authenticate a user",
    description="Sign in with Firebase Authentication and return the auth tokens.",
)
def login_user(
    payload: UserLogin,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict[str, Any]:
    """Authenticate a user with Firebase Auth and return tokens."""
    try:
        return service.login(payload)
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get(
    "/me",
    response_model=dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="Verify the supplied Firebase ID token and return the authenticated user's claims.",
)
def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict[str, Any]:
    """Return the authenticated user details from a verified Firebase ID token."""
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Authorization token is required")

    try:
        return service.verify_token(credentials.credentials)
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail=str(exc)) from exc
