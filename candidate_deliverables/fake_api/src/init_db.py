import psycopg2

conn = psycopg2.connect(
    dbname="truvi_db",
    user="truvi",
    password="truvi",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS bookings_raw (
    booking_id TEXT PRIMARY KEY,
    check_in_date DATE,
    check_out_date DATE,
    owner_company TEXT,
    owner_company_country TEXT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS currency_rates (
    currency TEXT PRIMARY KEY,
    rate_to_gbp NUMERIC
);
""")

conn.commit()
cur.close()
conn.close()
