from fastapi import APIRouter, Query, HTTPException
from datetime import datetime, date

from backend.models.user_models import LoginRequest
from backend.services.db import get_db_connection
from backend.services.dsm import compute_dsm

router = APIRouter()

#login
@router.post("/login")
def login(data: LoginRequest):
    if data.username == "admin" and data.password == "passward123":
        return {
            "message": "Login successful",
            "username": data.username,
            "role": "admin"
        }

    raise HTTPException(status_code=401, detail="Invalid username or password")

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
@router.get("/dsm")
def get_dsm(date: date):
    conn = get_db_connection()
    cursor = conn.cursor()

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

    timestamp, plant_id, schedule, generation = row

    result = compute_dsm(float(generation), float(schedule), 50)

    cursor.execute("""
        INSERT INTO dsm_records (
            timestamp, plant_id, schedule, actual, deviation, penalty
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        timestamp,
        plant_id,
        schedule,
        generation,
        result["deviation"],
        result["penalty"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "timestamp": timestamp,
        "plant_id": plant_id,
        "schedule": schedule,
        "actual": generation,
        "deviation": result["deviation"],
        "penalty": result["penalty"]
    }


# LOGOUT
@router.post("/logout")
def logout():
    return {
        "message": "User logged out successfully"
    }