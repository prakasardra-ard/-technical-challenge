from config import DB_CONFIG
import psycopg2

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()
cur.execute("SELECT * FROM bookings_raw;")
rows = cur.fetchall()
for row in rows:
    print(row)

cur.close()
conn.close()