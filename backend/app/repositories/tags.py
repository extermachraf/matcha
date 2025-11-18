# app/repositories/tag_manager.py

from sqlalchemy import create_engine, text
from flask import current_app
from app.repositories.connection import get_db_engine

# (Assuming get_db_engine() is available here)

def get_tag_ids_by_names(tag_names: list) -> dict:
    """
    Queries the database to map tag names (strings) to their corresponding IDs.
    
    Returns: {tag_name: tag_id}
    """
    engine = get_db_engine()
    
    # We use UNNEST and array input (standard PostgreSQL feature) for efficiency
    sql = """
        SELECT
            name, id
        FROM
            tags
        WHERE
            name = ANY(ARRAY[:tag_names]);
    """
    
    # Parameterization: Pass the list of names as an array parameter
    params = {'tag_names': tag_names} 
    
    found_tags = {}
    with engine.connect() as connection:
        result = connection.execute(text(sql), params).fetchall()
        
        for name, tag_id in result:
            found_tags[name] = tag_id
            
    return found_tags

