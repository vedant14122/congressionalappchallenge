-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Set timezone
SET timezone = 'America/Los_Angeles';

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_shelters_location ON shelters USING GIST (ST_SetSRID(ST_MakePoint(lon, lat), 4326));
CREATE INDEX IF NOT EXISTS idx_resources_location ON resources USING GIST (ST_SetSRID(ST_MakePoint(lon, lat), 4326));
CREATE INDEX IF NOT EXISTS idx_shelter_status_last_updated ON shelter_status(last_updated);
CREATE INDEX IF NOT EXISTS idx_status_changes_changed_at ON status_changes(changed_at);
