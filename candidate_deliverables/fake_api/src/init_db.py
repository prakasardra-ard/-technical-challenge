import psycopg2
from config import DB_CONFIG

def init_db():
    """Initialize database tables if they don't exist."""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
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
