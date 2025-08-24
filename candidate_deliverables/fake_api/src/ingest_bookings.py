import requests
import psycopg2
import logging
from datetime import datetime
from config import DB_CONFIG

API_URL = "http://localhost:5000/api/bookings"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def fetch_all_bookings(per_page=100, max_pages=None):
    """
    Fetch paginated booking data from the fake API.
    Returns a list of booking records.
    """
    all_data, page = [], 1
    while True:
        try:
            res = requests.get(API_URL, params={"page": page, "per_page": per_page})
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed on page {page}: {e}")
            break

        results = res.json().get("results", [])
        if not results:
            break

        all_data.extend(results)
        logging.info(f"Page {page}: Retrieved {len(results)} bookings.")
        page += 1

        if max_pages and page > max_pages:
            logging.warning("Reached max_pages limit.")
            break

    logging.info(f"Total bookings fetched: {len(all_data)}")
    return all_data

def insert_into_db(bookings):
    """
    Insert booking data into PostgreSQL database.
    Skips records with missing fields.
    """
    inserted = 0
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                for b in bookings:
                    required_fields = ("booking_id", "check_in_date", "check_out_date", "owner_company", "owner_company_country")
                    if not all(k in b for k in required_fields):
                        logging.warning(f"Skipping incomplete record: {b}")
                        continue

                    try:
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
                        inserted += 1
                    except Exception as row_error:
                        logging.warning(f"Failed to insert booking {b['booking_id']}: {row_error}")

        logging.info(f"Successfully inserted {inserted} bookings into bookings_raw.")
    except Exception as e:
        logging.error(f"Database insertion failed: {e}")

def ingest_bookings():
    bookings = fetch_all_bookings()
    if bookings:
        insert_into_db(bookings)
    else:
        logging.warning("No bookings fetched. Skipping DB insertion.")

if __name__ == "__main__":
    ingest_bookings()
