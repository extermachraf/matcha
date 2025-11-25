# app/repositories/tag_manager.py

from unittest import result
from sqlalchemy import create_engine, text
from flask import current_app, g
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


def get_user_tags_by_id(user_id: int) -> list:
    """
    Retrieves the list of tag names associated with a given user ID.
    
    Returns: [tag_name1, tag_name2, ...]
    """
    engine = get_db_engine()
    
    sql = """
        SELECT
            t.name
        FROM
            user_tags ut
        JOIN
            tags t ON ut.tag_id = t.id
        WHERE
            ut.user_id = :user_id;
    """
    
    params = {'user_id': user_id}
    
    user_tags = []
    with engine.connect() as connection:
        result = connection.execute(text(sql), params).fetchall()
        if not result:
            return []
        for (tag_name,) in result:
            user_tags.append(tag_name)
            
    return user_tags
