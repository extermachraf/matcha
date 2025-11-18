from sqlalchemy import create_engine, text
from flask import current_app
from datetime import datetime, timezone
from app.repositories.connection import get_db_engine

def update_or_insert_location(user_id: int, data: dict):
    """
    Performs an UPSERT (Update OR Insert) operation on the locations table.
    """
    engine = get_db_engine()
    
    # Define parameters with defaults for nullable fields
    params = {
        'user_id': user_id,
        'is_gps_enabled': data['is_gps_enabled'],
        'latitude': data.get('latitude'),
        'longitude': data.get('longitude'),
        'neighborhood': data.get('neighborhood'),
        'updated_at': datetime.now(timezone.utc)
    }

    # PostgreSQL UPSERT statement (INSERT ... ON CONFLICT UPDATE)
    sql = """
        INSERT INTO locations (user_id, is_gps_enabled, latitude, longitude, neighborhood, updated_at)
        VALUES (:user_id, :is_gps_enabled, :latitude, :longitude, :neighborhood, :updated_at)
        ON CONFLICT (user_id) DO UPDATE SET
            is_gps_enabled = EXCLUDED.is_gps_enabled,
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude,
            neighborhood = EXCLUDED.neighborhood,
            updated_at = EXCLUDED.updated_at
        WHERE 
            locations.user_id = EXCLUDED.user_id;
    """
    
    try:
        with engine.connect() as connection:
            connection.execute(text(sql), params)
            connection.commit()
            return True
    except Exception as e:
        raise Exception(f"Database UPSERT failed for location: {e}")