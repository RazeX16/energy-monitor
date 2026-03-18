import time
import random
from datetime import datetime
from backend.services.db import get_db_connection


def generate_data():
    print("Generator started...")

    while True:
        try:
        
            conn = get_db_connection()
            cursor = conn.cursor()
        

            timestamp = datetime.now()
            plant_id = 1
            frequency = round(random.uniform(49.5, 50.5), 2)
            generation = round(random.uniform(100, 150), 2)
            schedule = 120
            deviation = generation - schedule

            print("Inserting data...")

            cursor.execute("""
                INSERT INTO realtime_data
                (timestamp, plant_id, frequency, generation, schedule, deviation)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (timestamp, plant_id, frequency, generation, schedule, deviation))

            conn.commit()
            print(f"Inserted: {timestamp} | Gen: {generation} | Freq: {frequency}")

            cursor.close()
            conn.close()

            time.sleep(5)

        except Exception as e:
            print("Error:", e)
            break


if __name__ == "__main__":
    generate_data()