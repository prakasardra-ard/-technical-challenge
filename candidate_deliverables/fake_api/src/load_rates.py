import pandas as pd
import psycopg2
from psycopg2 import sql
from config import DB_CONFIG

def insert_gbp_rates(csv_path):
    """
    Load GBP currency rates from a CSV and insert into PostgreSQL.
    """
    try:
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip().str.lower()
        df["to_currency"] = df["to_currency"].str.strip().str.lower()
        df["from_currency"] = df["from_currency"].str.strip().str.upper()

        gbp_rates = df[df["to_currency"] == "gbp"].copy()
        gbp_rates = gbp_rates.dropna(subset=["from_currency", "rate"])

        if gbp_rates.empty:
            print("[INFO] No valid GBP rates found in the CSV.")
            return

        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                insert_query = sql.SQL("""
                    INSERT INTO currency_rates (currency, rate_to_gbp)
                    VALUES (%s, %s)
                    ON CONFLICT (currency) DO NOTHING
                """)
                inserted = 0
                for _, row in gbp_rates.iterrows():
                    cur.execute(insert_query, (row["from_currency"], row["rate"]))
                    inserted += 1

        print(f"[INFO] Successfully inserted {inserted} GBP rates into currency_rates.")

    except (psycopg2.Error, pd.errors.ParserError) as e:
        print(f"[ERROR] Database or CSV error: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected failure: {e}")

def ingest_rates():
    insert_gbp_rates("Data/currency_rates.csv")

if __name__ == "__main__":
    ingest_rates()
