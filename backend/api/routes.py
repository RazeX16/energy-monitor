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
from datetime import datetime
from fastapi import Query

@router.get("/historical")
def get_historical_report(
    start: datetime = Query(...), 
    end: datetime = Query(...)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # We add a WHERE clause to filter the data by your parameters
        query = """
            SELECT 
                time_bucket('15 minutes', timestamp) AS block,
                AVG(generation), AVG(frequency), SUM(deviation)
            FROM realtime_data
            WHERE timestamp >= %s AND timestamp <= %s
            GROUP BY block
            ORDER BY block DESC;
        """
        cursor.execute(query, (start, end))
        rows = cursor.fetchall()

        return [
            {"time": r[0], "gen": round(r[1], 2), "freq": round(r[2], 2), "dev": r[3]} 
            for r in rows
        ]
    finally:
        cursor.close()
        conn.close()



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
