import psycopg2

conn = psycopg2.connect(
    dbname="truvi_db",
    user="truvi",
    password="truvi",
    host="localhost",
    port="5432"
)

cur = conn.cursor()
cur.execute("SELECT * FROM bookings_raw;")
rows = cur.fetchall()
for row in rows:
    print(row)

cur.close()
conn.close()
