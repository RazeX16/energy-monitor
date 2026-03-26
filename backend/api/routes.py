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
from fastapi import APIRouter, Query
from datetime import date, datetime, time, timedelta
from backend.services.db import get_db_connection

router = APIRouter()

@router.get("/historical")
def get_historical(
    start_date: date = Query(...),
    end_date: date = Query(...)
):
    conn = get_db_connection()
    cursor = conn.cursor()

    start_datetime = datetime.combine(start_date, time.min)
    end_datetime = datetime.combine(end_date + timedelta(days=1), time.min)

    cursor.execute("""
        SELECT timestamp, generation, schedule, frequency, deviation
        FROM realtime_data
        WHERE timestamp >= %s AND timestamp < %s
        ORDER BY timestamp ASC
    """, (start_datetime, end_datetime))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "timestamp": str(row[0]),
            "generation": row[1],
            "schedule": row[2],
            "frequency": row[3],
            "deviation": row[4]
        })

    return {"data": data}

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