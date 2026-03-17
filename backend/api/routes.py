from fastapi import APIRouter
from backend.models.user_models import LoginRequest
from backend.services.db import get_db_connection

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

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, generation, schedule, frequency, deviation
        FROM realtime_data
        ORDER BY timestamp DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return {
            "timestamp": row[0],
            "generation": row[1],
            "schedule": row[2],
            "frequency": row[3],
            "deviation": row[4]
        }

    return {"message": "No realtime data available"}


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