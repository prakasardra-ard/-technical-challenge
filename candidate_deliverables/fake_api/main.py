import psycopg2
import pandas as pd
from config import DB_CONFIG
from src.load_rates import ingest_rates
from src.ingest_bookings import ingest_bookings
from src.transform_data import transform_data

def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings_raw (
            booking_id TEXT PRIMARY KEY,
            check_in_date DATE,
            check_out_date DATE,
            owner_company TEXT,
            owner_company_country TEXT
        );

        CREATE TABLE IF NOT EXISTS currency_rates (
            currency TEXT PRIMARY KEY,
            rate_to_gbp NUMERIC
        );

        CREATE TABLE IF NOT EXISTS final_summary (
            booking_id TEXT PRIMARY KEY,
            check_in_date DATE,
            check_out_date DATE,
            owner_company TEXT,
            owner_company_country TEXT,
            total_days INTEGER,
            rate_to_gbp NUMERIC
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def main():
    init_db()
    ingest_rates()
    ingest_bookings()
    df = transform_data()
    #print(df.head())
    print(df.head(20))  # Show first 20 rows
    print(df.tail(10))  # Show last 10 rows
    print(df.shape)     # Show (rows, columns) count


if __name__ == "__main__":
    main()