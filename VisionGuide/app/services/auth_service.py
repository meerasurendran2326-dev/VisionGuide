from typing import Any

import requests
from fastapi import HTTPException, status
from firebase_admin import auth as firebase_auth

from app.config import settings
from app.firebase import initialize_firebase
from app.models.user import UserCreate, UserLogin, UserOut
from app.services.firestore_service import FirestoreService


class AuthService:
    """Authentication service for Firebase-based user registration and login."""

    def __init__(self) -> None:
        """Create the service with access to the Firestore persistence layer."""
        self.firestore_service = FirestoreService()

    def register(self, payload: UserCreate) -> UserOut:
        """Create a Firebase Auth account and persist the user profile in Firestore."""
        if not initialize_firebase():
            raise HTTPException(status_code=503, detail="Firebase is not available")

        try:
            user_record = firebase_auth.create_user(
                email=str(payload.email),
                password=payload.password,
                display_name=payload.name,
            )
        except Exception as exc:  # pragma: no cover - depends on Firebase runtime availability
            raise HTTPException(status_code=400, detail=f"Registration failed: {exc}") from exc

        user_data = {
            "uid": user_record.uid,
            "name": payload.name,
            "email": str(payload.email),
            "emergency_contact": payload.emergency_contact,
        }

        try:
            self.firestore_service.save_user(user_record.uid, user_data)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Failed to save user profile: {exc}") from exc

        return UserOut(**user_data)

    def login(self, payload: UserLogin) -> dict[str, Any]:
        """Authenticate a user using Firebase Auth REST sign-in and return tokens."""
        if not initialize_firebase():
            raise HTTPException(status_code=503, detail="Firebase is not available")

        if not settings.FIREBASE_WEB_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="FIREBASE_WEB_API_KEY is not configured in the environment",
            )

        url = (
            "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
            f"?key={settings.FIREBASE_WEB_API_KEY}"
        )
        body = {
            "email": str(payload.email),
            "password": payload.password,
            "returnSecureToken": True,
        }

        try:
            response = requests.post(url, json=body, timeout=10)
            response.raise_for_status()
            data: dict[str, Any] = response.json()
        except requests.RequestException as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            ) from exc

        return {
            "idToken": data.get("idToken"),
            "refreshToken": data.get("refreshToken"),
            "uid": data.get("localId"),
        }

    def verify_token(self, id_token: str) -> dict[str, Any]:
        """Verify a Firebase ID token and return the decoded claims."""
        if not initialize_firebase():
            raise HTTPException(status_code=503, detail="Firebase is not available")

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
        except Exception as exc:
            raise HTTPException(status_code=401, detail=f"Invalid or expired token: {exc}") from exc

        return {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "name": decoded_token.get("name"),
            "claims": decoded_token,
        }
