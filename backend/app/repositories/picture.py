from sqlalchemy import create_engine, text
from flask import current_app
from app.repositories.connection import get_db_engine


def add_new_picture(user_id: int, file_path: str, is_profile_picture: bool = False):
    """
    Inserts a new picture record into the pictures table.
    """
    engine = get_db_engine()
    
    
    next_order_sql = "SELECT COALESCE(MAX(upload_order), 0) + 1 FROM pictures WHERE user_id = :user_id;"
    
    insert_sql = """
        INSERT INTO pictures (user_id, file_path, is_profile_picture, upload_order, created_at)
        VALUES (:user_id, :file_path, :is_profile_pic, :upload_order, CURRENT_TIMESTAMP)
        RETURNING id;
    """
    with engine.connect() as connection:
        # Start transaction
        trans = connection.begin()
        
        try:
            # 1. Get Next Order Number
            next_order = connection.execute(text(next_order_sql), {'user_id': user_id}).scalar_one()
            
            # 2. Insert Picture Record
            params = {
                'user_id': user_id,
                'file_path': file_path,
                'is_profile_pic': is_profile_picture,
                'upload_order': next_order
            }
            result = connection.execute(text(insert_sql), params)
            new_pic_id = result.scalar_one()
            
            trans.commit()
            return new_pic_id
        except Exception:
            trans.rollback()
            raise
        
def count_user_pictures(user_id: int) -> int:
    """
    Counts the total number of pictures currently associated with a user ID.
    """
    engine = get_db_engine()
    
    sql = """
        SELECT COUNT(id)
        FROM pictures
        WHERE user_id = :user_id;
    """
    
    params = {'user_id': user_id}
    
    with engine.connect() as connection:
        # scalar_one() safely retrieves the single count value
        count = connection.execute(text(sql), params).scalar_one()
        
    return count