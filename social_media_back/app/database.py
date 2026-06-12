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

cursor.execute("""
CREATE TABLE IF NOT EXISTS posts(
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    published BOOLEAN DEFAULT TRUE,
    rating INTEGER
)
""")

conn.commit()

print("Table created successfully")