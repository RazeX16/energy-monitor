import psycopg2
from backend.services.auth import hash_password
<<<<<<< HEAD
=======

>>>>>>> b24e80d (changes made)

def get_db_connection():
    conn = psycopg2.connect(
        database="energy-monitor",
        user="postgres",
        password="Ajdil@29",
<<<<<<< HEAD
        host="192.168.1.175",
=======
        host="192.168.1.51",
>>>>>>> b24e80d (changes made)
        port="5432"
    )
    return conn

users = {
    "admin": {
        "username": "admin",
        "password": hash_password("1234"),
        "role": "admin"
    }
}