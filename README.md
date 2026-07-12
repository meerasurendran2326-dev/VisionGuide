# VisionGuide AI Backend

This backend provides a production-ready FastAPI foundation for the VisionGuide AI project.

## Features
- Firebase Admin SDK initialization
- Firestore-backed user profiles, locations, and SOS records
- Authentication endpoints for registration and login
- Live location storage and retrieval
- SOS submission endpoint
- Swagger UI documentation via FastAPI

## Project Structure

backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── firebase.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── location.py
│   │   └── sos.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── firestore_service.py
│   ├── models/
│   │   ├── user.py
│   │   ├── location.py
│   │   └── sos.py
│   └── utils/
├── requirements.txt
├── .env
├── README.md
└── serviceAccountKey.json

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place your Firebase service account JSON as `serviceAccountKey.json` in the backend folder.
4. Update `.env` if needed.

## Run the server

```bash
uvicorn app.main:app --reload
```

Then open:
- Swagger docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

### Auth
- POST /auth/register
- POST /auth/login

### Location
- POST /location
- GET /location/{user_id}

### SOS
- POST /sos

## Flutter Request Examples

### Register
```json
{
  "name": "Asha",
  "email": "asha@example.com",
  "password": "secret123",
  "emergency_contact": "+919999999999"
}
```

### Login
```json
{
  "email": "asha@example.com",
  "password": "secret123"
}
```

### Save location
```json
{
  "userId": "abc123",
  "latitude": 10.523,
  "longitude": 76.214
}
```

### Send SOS
```json
{
  "userId": "abc123",
  "latitude": 10.523,
  "longitude": 76.214
}
```
