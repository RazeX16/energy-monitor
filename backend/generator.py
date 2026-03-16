import time
import random
from datetime import datetime
from services.db import get_db_connection


def generate_data():

    conn = get_db_connection()
    cursor = conn.cursor()

    while True:

        timestamp = datetime.now()
        plant_id = 1
        frequency = round(random.uniform(49.8, 50.2), 2)
        generation = round(random.uniform(110, 130), 2)
        schedule = 115
        deviation = generation - schedule

        cursor.execute(
            """
            INSERT INTO realtime_data
            (timestamp, plant_id, frequency, generation, schedule, deviation)
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (timestamp, plant_id, frequency, generation, schedule, deviation)
        )

        conn.commit()

        print("Inserted:", timestamp, frequency, generation)

        time.sleep(5)


if __name__ == "__main__":
    generate_data()