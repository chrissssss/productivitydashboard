import os
import time
import random
import psycopg2
from psycopg2 import OperationalError

def create_connection():
    """Create a database connection."""
    conn = None
    while not conn:
        try:
            conn = psycopg2.connect(
                dbname=os.environ.get("POSTGRES_DB"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD"),
                host=os.environ.get("POSTGRES_HOST"),
            )
        except OperationalError as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
    return conn

def main():
    """Main function to generate and insert metrics."""
    conn = create_connection()
    print("Successfully connected to PostgreSQL!")
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    value FLOAT NOT NULL
                );
            """)
            conn.commit()
            print("Table 'metrics' is ready.")

            while True:
                value = random.uniform(0.0, 100.0)
                cur.execute(
                    "INSERT INTO metrics (value) VALUES (%s)",
                    (value,)
                )
                cur.execute(
                    "INSERT INTO live_metrics (value) VALUES (%s)",
                    (value,)
                )
                conn.commit()
                print(f"Inserted new metric value into both tables: {value}")
                time.sleep(5)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()