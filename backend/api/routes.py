from fastapi import APIRouter
from models.user_models import LoginRequest

router = APIRouter()


# LOGIN
@router.post("/login")
def login(data: LoginRequest):
    return {
        "message": "Login API placeholder",
        "username": data.username
    }


# REALTIME DATA
@router.get("/realtime")
def get_realtime():
    return {
        "timestamp": "2026-03-12T10:00:00",
        "generation": 120,
        "schedule": 115,
        "frequency": 49.9,
        "deviation": 5
    }


# HISTORICAL DATA
@router.get("/historical")
def get_historical():
    return {
        "data": [
            {"time": "10:00", "generation": 120, "schedule": 115},
            {"time": "10:15", "generation": 118, "schedule": 115}
        ]
    }


# DSM DATA
@router.get("/dsm")
def get_dsm():
    return {
        "schedule": 115,
        "actual": 120,
        "deviation": 5,
        "penalty": 250
    }


# LOGOUT
@router.post("/logout")
def logout():
    return {
        "message": "User logged out successfully"
    }