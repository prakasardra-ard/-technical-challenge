import requests
import psycopg2
from datetime import datetime

API_URL = "http://localhost:5000/api/bookings"
DB_CONFIG = {
    "dbname": "truvi_db",
    "user": "truvi",
    "password": "truvi",
    "host": "localhost"
}

def fetch_all_bookings():
    """Fetch paginated booking data from the fake API."""
    all_data, page = [], 1
    while True:
        try:
            res = requests.get(API_URL, params={"page": page, "per_page": 100})
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] API request failed on page {page}: {e}")
            break
        results = res.json().get("results", [])
        if not results:
            break
        all_data.extend(results)
        page += 1
    print(f"[INFO] Fetched {len(all_data)} bookings from API.")
    return all_data

def insert_into_db(bookings):
    """Insert booking data into PostgreSQL database."""
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                for b in bookings:
                    cur.execute("""
                        INSERT INTO bookings_raw (
                            booking_id,
                            check_in_date,
                            check_out_date,
                            owner_company,
                            owner_company_country
                        ) VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                    """, (
                        b["booking_id"],
                        datetime.fromisoformat(b["check_in_date"]).date(),
                        datetime.fromisoformat(b["check_out_date"]).date(),
                        b["owner_company"],
                        b["owner_company_country"]
                    ))
        print(f"[INFO] Inserted {len(bookings)} bookings into the database.")
    except Exception as e:
        print(f"[ERROR] Database insertion failed: {e}")

if __name__ == "__main__":
    bookings = fetch_all_bookings()
    if bookings:
        insert_into_db(bookings)
