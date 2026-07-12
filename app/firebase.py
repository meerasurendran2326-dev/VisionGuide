import json
from pathlib import Path
from typing import Any, Optional

import firebase_admin
from firebase_admin import auth, credentials, firestore
from google.cloud.firestore_v1.client import Client as FirestoreClient

from app.config import settings

firebase_app: Optional[Any] = None
firebase_auth: Optional[Any] = None
firestore_db: Optional[FirestoreClient] = None
firebase_initialized = False
firebase_error_message: Optional[str] = None


def initialize_firebase() -> bool:
    """Initialize Firebase Admin SDK and Firestore once for the application lifecycle."""
    global firebase_app, firebase_auth, firestore_db, firebase_initialized, firebase_error_message

    if firebase_initialized and firebase_app is not None and firestore_db is not None:
        return True

    credential_path = Path(settings.FIREBASE_SERVICE_ACCOUNT_PATH)
    if not credential_path.exists():
        firebase_error_message = (
            f"Firebase service account file not found at {credential_path}. "
            "Provide a valid file or update FIREBASE_SERVICE_ACCOUNT_PATH."
        )
        return False

    try:
        with credential_path.open("r", encoding="utf-8") as handle:
            service_account = json.load(handle)

        if not firebase_admin._apps:
            firebase_app = firebase_admin.initialize_app(
                credentials.Certificate(service_account),
                {"projectId": service_account.get("project_id") or settings.FIREBASE_PROJECT_ID},
            )
        else:
            firebase_app = firebase_admin.get_app()

        firebase_auth = auth
        firestore_db = firestore.client()
        firebase_initialized = True
        firebase_error_message = None
        return True
    except FileNotFoundError as exc:
        firebase_error_message = f"Firebase credentials file could not be read: {exc}"
        return False
    except json.JSONDecodeError as exc:
        firebase_error_message = f"Firebase credentials JSON is invalid: {exc}"
        return False
    except ValueError as exc:
        firebase_error_message = f"Firebase initialization failed because the credentials are invalid: {exc}"
        return False
    except Exception as exc:  # pragma: no cover - defensive fallback for runtime issues
        firebase_error_message = f"Firebase initialization failed: {exc}"
        return False


__all__ = ["initialize_firebase", "firebase_app", "firebase_auth", "firestore_db", "firebase_initialized"]
