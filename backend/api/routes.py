from fastapi import APIRouter, Query, HTTPException
from datetime import datetime, date

from backend.models.user_models import LoginRequest
from backend.services.db import get_db_connection
from backend.services.dsm import compute_dsm

router = APIRouter()

#login
from fastapi import APIRouter
from backend.models.user_models import LoginRequest


@router.post("/login")
def login(data: LoginRequest):
    if data.username == "admin" and data.password == "admin123":
        return {
            "message": "Login successful",
            "token": "test-token",
            "username": data.username,
            "role": "admin"
        }
    return {
        "message": "Invalid username or password"
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
from fastapi import APIRouter, Query
from datetime import date, datetime, time, timedelta
from backend.services.db import get_db_connection


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
from datetime import timedelta # Make sure this is imported at the top of your file!

@router.get("/dsm")
def get_dsm(date: date):
    conn = get_db_connection()
    cursor = conn.cursor()

    # --- 1. GET LATEST RECORD (For Top Cards) ---
    cursor.execute("""
        SELECT timestamp, plant_id, schedule, generation, frequency
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

    # Unpack the row (Now including frequency!)
    timestamp, plant_id, schedule, generation, frequency = row
    
    # Calculate DSM Penalty
    result = compute_dsm(float(generation), float(schedule), 50)

    # Save the calculation to the database
   # Save the calculation to the database
    cursor.execute("""
        INSERT INTO DSM_records (
            timestamp, plant_id, schedule, actual, deviation, penalty
        ) VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (timestamp, plant_id) 
        DO UPDATE SET 
            schedule = EXCLUDED.schedule,
            actual = EXCLUDED.actual,
            deviation = EXCLUDED.deviation,
            penalty = EXCLUDED.penalty;
    """, (
        timestamp,
        plant_id,
        schedule,      # This maps to the 'schedule' column
        generation,    # This maps to the 'actual' column
        result["deviation"],
        result["penalty"]
    ))
    
    conn.commit()

    # --- 2. GET HISTORICAL DATA (For the Chart) ---
    # Calculate the time 2 hours before the most recent timestamp
    two_hours_ago = timestamp - timedelta(hours=2)

    # Fetch all records within that 2-hour window, ordered from oldest to newest
    cursor.execute("""
        SELECT timestamp, schedule, generation
        FROM realtime_data
        WHERE timestamp >= %s AND timestamp <= %s
        ORDER BY timestamp ASC
    """, (two_hours_ago, timestamp))

    chart_rows = cursor.fetchall()

    # Format the data into lists for Chart.js
    labels = []
    scheduled_data = []
    actual_data = []

    for r in chart_rows:
        row_time = r[0]
        labels.append(row_time.strftime("%H:%M")) # Converts full datetime to just "10:15"
        scheduled_data.append(r[1])
        actual_data.append(r[2])

    chart_data = {
        "labels": labels,
        "scheduled": scheduled_data,
        "actual": actual_data
    }

    cursor.close()
    conn.close()

    # --- 3. RETURN EVERYTHING TO THE FRONTEND ---
    return {
        "timestamp": timestamp,
        "plant_id": plant_id,
        "schedule": schedule,
        "actual": generation,
        "frequency": frequency,
        "deviation": result["deviation"],
        "penalty": result["penalty"],
        "chartData": chart_data  # The frontend will inject this straight into the graph
    }


# LOGOUT
@router.post("/logout")
def logout():
    return {
        "message": "User logged out successfully"
    }