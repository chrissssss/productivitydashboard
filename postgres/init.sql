-- Create a new table for live data
CREATE TABLE IF NOT EXISTS live_metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    value FLOAT NOT NULL
);

-- Create the trigger function
CREATE OR REPLACE FUNCTION notify_new_record()
RETURNS TRIGGER AS $$
DECLARE
    notification_payload TEXT;
BEGIN
    notification_payload := json_build_object(
        'record_id', NEW.id,
        'value', NEW.value,
        'timestamp', NEW.timestamp
    )::text;

    PERFORM pg_notify('influx_feed', notification_payload);
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Define the trigger on the new table
-- Make sure the trigger is not created if it already exists
DO $$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'new_record_to_influx') THEN
      CREATE TRIGGER new_record_to_influx
      AFTER INSERT ON live_metrics
      FOR EACH ROW
      EXECUTE FUNCTION notify_new_record();
   END IF;
END
$$;