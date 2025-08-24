from config import DB_CONFIG
import psycopg2
import pandas as pd

def transform_data():
    try:
        with open("src/transform.sql", "r") as f:
            sql_script = f.read()

        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_script)
            print("[INFO] Transformation SQL executed successfully.")

        # Fetch transformed data
        query = "SELECT * FROM final_summary;"
        df = pd.read_sql(query, conn)
        return df

    except Exception as e:
        print(f"[ERROR] Failed to execute transformation SQL: {e}")
        return None
