from datetime import datetime
from typing import Any

from firebase_admin import firestore as firestore_admin

import app.firebase as firebase


class FirestoreService:
    """Service layer for Firestore access to users, locations, and SOS records."""

    def __init__(self) -> None:
        """Create the service with a Firestore client reference when available."""
        self.db = None

    def _ensure_db(self) -> Any:
        """Ensure Firebase is initialized and return a Firestore client."""
        if not firebase.initialize_firebase():
            raise RuntimeError("Firebase initialization failed. Check credentials and configuration.")

        if firebase.firestore_db is None:
            raise RuntimeError("Firestore client is not initialized")

        self.db = firebase.firestore_db
        return self.db

    def _normalize_value(self, value: Any) -> Any:
        """Convert Firestore-specific values into JSON-serializable values."""
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, dict):
            return {key: self._normalize_value(item) for key, item in value.items()}
        if isinstance(value, list):
            return [self._normalize_value(item) for item in value]
        return value

    def _document_to_dict(self, document: Any) -> dict[str, Any] | None:
        """Convert a Firestore document snapshot to a plain dictionary."""
        if document is None or not getattr(document, "exists", False):
            return None
        data = document.to_dict()
        normalized_data = self._normalize_value(data)
        return dict(normalized_data) if isinstance(normalized_data, dict) else normalized_data

    def save_user(self, uid: str, user_data: dict[str, Any]) -> dict[str, Any]:
        """Create or overwrite a user document in the users collection."""
        db = self._ensure_db()
        try:
            db.collection("users").document(uid).set(user_data)
            return {"uid": uid, **user_data}
        except Exception as exc:
            raise RuntimeError(f"Failed to save user document: {exc}") from exc

    def get_user(self, uid: str) -> dict[str, Any] | None:
        """Retrieve a user document as a plain dictionary."""
        db = self._ensure_db()
        try:
            document = db.collection("users").document(uid).get()
            return self._document_to_dict(document)
        except Exception as exc:
            raise RuntimeError(f"Failed to fetch user document: {exc}") from exc

    def update_location(self, user_id: str, latitude: float, longitude: float) -> dict[str, Any]:
        """Save a new location update for a user using Firestore server timestamps."""
        db = self._ensure_db()
        try:
            document_ref = db.collection("locations").document(user_id)
            document_ref.set(
                {
                    "userId": user_id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "updatedAt": firestore_admin.SERVER_TIMESTAMP,
                },
                merge=True,
            )
            refreshed_document = document_ref.get()
            payload = self._document_to_dict(refreshed_document)
            if payload is None:
                raise RuntimeError("Location document could not be read after save")
            return payload
        except Exception as exc:
            raise RuntimeError(f"Failed to update location: {exc}") from exc

    def get_latest_location(self, user_id: str) -> dict[str, Any] | None:
        """Return the latest saved location for a user."""
        db = self._ensure_db()
        try:
            document = db.collection("locations").document(user_id).get()
            return self._document_to_dict(document)
        except Exception as exc:
            raise RuntimeError(f"Failed to fetch latest location: {exc}") from exc

    def create_sos(self, user_id: str, latitude: float, longitude: float) -> dict[str, Any]:
        """Create a new SOS document in the sos collection with a server timestamp."""
        db = self._ensure_db()
        try:
            document_ref = db.collection("sos").document()
            document_ref.set(
                {
                    "userId": user_id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "timestamp": firestore_admin.SERVER_TIMESTAMP,
                    "status": "pending",
                }
            )
            refreshed_document = document_ref.get()
            payload = self._document_to_dict(refreshed_document)
            if payload is None:
                raise RuntimeError("SOS document could not be read after create")
            return payload
        except Exception as exc:
            raise RuntimeError(f"Failed to create SOS record: {exc}") from exc

    def get_sos_history(self, user_id: str) -> list[dict[str, Any]]:
        """Return the SOS history for a user as a list of dictionaries."""
        db = self._ensure_db()
        try:
            documents = (
                db.collection("sos")
                .where("userId", "==", user_id)
                .order_by("timestamp", direction=firestore_admin.Query.DESCENDING)
                .stream()
            )
            return [
                item
                for item in (self._document_to_dict(document) for document in documents)
                if item is not None
            ]
        except Exception as exc:
            raise RuntimeError(f"Failed to fetch SOS history: {exc}") from exc

    # Backward-compatible wrappers for the existing route/service layer.
    def get_user_doc(self, uid: str) -> dict[str, Any] | None:
        """Backward-compatible alias for get_user."""
        return self.get_user(uid)

    def create_user(self, uid: str, user_data: dict[str, Any]) -> dict[str, Any]:
        """Backward-compatible alias for save_user."""
        return self.save_user(uid, user_data)

    def save_location(self, user_id: str, latitude: float, longitude: float) -> dict[str, Any]:
        """Backward-compatible alias for update_location."""
        return self.update_location(user_id, latitude, longitude)

    def save_sos(self, user_id: str, latitude: float, longitude: float) -> dict[str, Any]:
        """Backward-compatible alias for create_sos."""
        return self.create_sos(user_id, latitude, longitude)
