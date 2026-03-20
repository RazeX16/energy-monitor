from fastapi import APIRouter, Query
from datetime import datetime

from backend.models.user_models import LoginRequest
from backend.services.db import get_db_connection
from backend.services.dsm import compute_dsm

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
def get_historical_report(
    start: datetime = Query(...), 
    end: datetime = Query(...)
):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
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
            {
                "time": r[0],
                "gen": round(r[1], 2),
                "freq": round(r[2], 2),
                "dev": r[3]
            }
            for r in rows
        ]
    finally:
        cursor.close()
        conn.close()


# DSM DATA
# DSM DATA
@router.get("/dsm")
<<<<<<< HEAD
def get_dsm(date: str):
=======
def get_dsm():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT generation, schedule
        FROM realtime_data
        ORDER BY timestamp DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return {"message": "No realtime data available"}

    generation = float(row[0])
    schedule = float(row[1])

    rate = 50  # DSM rate (configurable later)

    return compute_dsm(generation, schedule, rate)
>>>>>>> c35bbb8 (dsm is done)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch latest record for given date
    cursor.execute("""
        SELECT timestamp, plant_id, schedule, generation
        FROM realtime_data
        WHERE DATE(timestamp) = %s
        ORDER BY timestamp DESC
        LIMIT 1
    """, (date,))

    row = cursor.fetchone()

    if not row:
        cursor.close()
        conn.close()
        return {"message": "No data found for given date"}

    timestamp, plant_id, schedule, actual = row

    # DSM Calculation
    deviation = actual - schedule
    penalty = deviation * 50  # static rate for now

    # Store in DSM_records
    cursor.execute("""
        INSERT INTO DSM_records (
            timestamp, plant_id, schedule, actual, deviation, penalty
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (timestamp, plant_id, schedule, actual, deviation, penalty))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "timestamp": timestamp,
        "plant_id": plant_id,
        "schedule": schedule,
        "actual": actual,
        "deviation": deviation,
        "penalty": penalty
    }

# LOGOUT
@router.post("/logout")
def logout():
    return {
        "message": "User logged out successfully"
    }
