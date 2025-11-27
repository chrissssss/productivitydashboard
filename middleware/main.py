import os
import time
import json
import select
import psycopg2
from psycopg2 import OperationalError
import asyncio
import websockets

def create_postgres_connection():
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
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        except OperationalError as e:
            print(f"PostgreSQL connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
    return conn

async def push_to_grafana(data):
    """Pushes data to the Grafana Live stream."""
    stream_id = 'my_stream_id'
    grafana_url = f"ws://grafana:3000/api/live/push/{stream_id}"
    
    try:
        async with websockets.connect(grafana_url) as websocket:
            # The payload should be a JSON object with a 'fields' array
            # containing key-value pairs for the data.
            grafana_payload = {
                "fields": [
                    {"name": "time", "values": [data["timestamp"]]},
                    {"name": "value", "values": [float(data["value"])]}
                ]
            }
            await websocket.send(json.dumps(grafana_payload))
            print(f"Pushed to Grafana Live: {data['value']}")
    except Exception as e:
        print(f"Failed to push to Grafana Live: {e}")

def main():
    """Main function to listen for notifications and push to Grafana Live."""
    conn = create_postgres_connection()
    print("Successfully connected to PostgreSQL!")

    try:
        with conn.cursor() as cur:
            cur.execute("LISTEN influx_feed;")
            print("Listening on channel 'influx_feed'...")

            while True:
                if select.select([conn], [], [], 5) == ([], [], []):
                    print("No new notifications...")
                else:
                    conn.poll()
                    while conn.notifies:
                        notify = conn.notifies.pop(0)
                        print(f"Received notification: {notify.payload}")
                        
                        payload_data = json.loads(notify.payload)
                        
                        # Run the async push function
                        asyncio.run(push_to_grafana(payload_data))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("PostgreSQL connection closed.")

if __name__ == "__main__":
    main()