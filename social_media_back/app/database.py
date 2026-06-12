import psycopg

conn = psycopg.connect(
    host="localhost",
    dbname="socialmedia",
    user="postgres",
    password="12345678",
    port=5432
)

cursor = conn.cursor()

print("Database connected successfully")