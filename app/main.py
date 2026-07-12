from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.firebase import initialize_firebase
from app.routes import auth, location, sos

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="VisionGuide AI backend for accessibility and emergency assistance features.",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(location.router)
app.include_router(sos.router)


@app.on_event("startup")
def startup_event() -> None:
    """Initialize Firebase once when the application starts."""
    initialize_firebase()


@app.get("/", tags=["Health"])
def root() -> dict[str, str]:
    """Return a basic API welcome message and documentation link."""
    return {
        "message": "VisionGuide AI backend is running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health() -> dict[str, object]:
    """Return the health status of the API and Firebase initialization state."""
    return {
        "status": "ok",
        "firebase_initialized": initialize_firebase(),
    }
