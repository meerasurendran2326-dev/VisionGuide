# VisionGuide AI Backend

## Overview
Backend services for the VisionGuide AI application.

## Features
- Firebase Authentication
- Cloud Firestore Integration
- User Registration & Login
- Live Location Storage
- SOS Emergency System
- REST APIs using FastAPI

## Tech Stack
- Python
- FastAPI
- Firebase Admin SDK
- Cloud Firestore
- Uvicorn

## API Endpoints
- POST /auth/register
- POST /auth/login
- POST /location
- POST /sos

## Setup
1. Clone the repository
2. Install requirements
3. Configure `.env`
4. Add `serviceAccountKey.json`
5. Run:
   uvicorn app.main:app --reload
