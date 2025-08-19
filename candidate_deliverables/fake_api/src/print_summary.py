import psycopg2

conn = psycopg2.connect(dbname="truvi_db", user="truvi", password="truvi", host="localhost")
cur = conn.cursor()
cur.execute("SELECT * FROM final_summary LIMIT 10")
rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()
