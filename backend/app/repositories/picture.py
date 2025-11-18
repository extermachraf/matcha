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

def set_main_profile_picture(user_id: int, picture_id: int):
    """
    Atomically sets the designated picture as the profile picture 
    and clears the flag from all others belonging to the user.
    """
    engine = get_db_engine()
    
    # 1. SQL to reset ALL other pictures for the user (Set is_profile_picture = FALSE)
    reset_sql = "UPDATE pictures SET is_profile_picture = FALSE WHERE user_id = :user_id;"
    
    # 2. SQL to set the specific picture as the main one
    set_sql = """
        UPDATE pictures
        SET is_profile_picture = TRUE
        WHERE user_id = :user_id AND id = :picture_id
        RETURNING id;
    """
    
    with engine.connect() as connection:
        trans = connection.begin()
        try:
            # Step 1: Reset all flags
            connection.execute(text(reset_sql), {'user_id': user_id})
            
            # Step 2: Set the new flag
            result = connection.execute(text(set_sql), {'user_id': user_id, 'picture_id': picture_id})
            
            # If rowcount is 0, the picture ID was wrong or didn't belong to the user
            if result.rowcount == 0:
                trans.rollback()
                raise ValueError("Picture not found or does not belong to the user.")

            trans.commit()
            return True
        except Exception:
            trans.rollback()
            raise
        
def delete_picture_record(user_id: int, picture_id: int):
    """
    Deletes the picture record and returns its file path for filesystem deletion.
    """
    engine = get_db_engine()
    
    # SQL to DELETE the record and RETURNING the file_path
    sql = """
        DELETE FROM pictures
        WHERE id = :picture_id AND user_id = :user_id
        RETURNING file_path, is_profile_picture;
    """
    
    params = {'user_id': user_id, 'picture_id': picture_id}
    
    with engine.connect() as connection:
        trans = connection.begin()
        try:
            result = connection.execute(text(sql), params).fetchone()
            
            if result is None:
                trans.rollback()
                # Picture not found or does not belong to the user
                raise ValueError("Picture not found or unauthorized deletion attempt.")
            
            file_path = result[0]
            is_profile_picture = result[1]
            
            # MANDATORY CHECK: Prevent deleting the last remaining picture if required by your logic
            # This requires a SELECT COUNT(*) query before the DELETE (omitted for brevity).
            
            # Commit the database deletion
            trans.commit()
            return file_path, is_profile_picture
        except Exception:
            trans.rollback()
            raise
        
def get_user_pictures(user_id: int) -> list:
    """
    Retrieves all pictures for a given user, ordered by upload_order.
    """
    engine = get_db_engine()
    
    sql = """
        SELECT id, file_path, is_profile_picture, upload_order, created_at
        FROM pictures
        WHERE user_id = :user_id
        ORDER BY upload_order ASC;
    """
    
    params = {'user_id': user_id}
    
    with engine.connect() as connection:
        result = connection.execute(text(sql), params).fetchall()
        
        pictures = []
        for row in result:
            pictures.append({
                'id': row[0],
                'file_path': row[1],
                'is_profile_picture': row[2],
                'upload_order': row[3],
                'created_at': row[4].isoformat()  # Convert datetime to ISO string
            })
            
    return pictures

def reorder_user_pictures(user_id: int):
    """
    Updates the upload_order column for all remaining pictures for a user
    to ensure a continuous sequence (1, 2, 3, ...).
    """
    engine = get_db_engine()

    # The SQL uses ROW_NUMBER() to generate a new sequential order based on creation time.
    sql = """
        WITH RankedPictures AS (
            SELECT
                id,
                ROW_NUMBER() OVER (ORDER BY created_at ASC) as new_order
            FROM
                pictures
            WHERE
                user_id = :user_id
        )
        UPDATE pictures
        SET upload_order = RankedPictures.new_order
        FROM RankedPictures
        WHERE pictures.id = RankedPictures.id AND pictures.user_id = :user_user_id;
    """
    
    # We pass the user_id twice to ensure both the CTE and the final UPDATE use it securely
    params = {'user_id': user_id, 'user_user_id': user_id} 
    
    with engine.connect() as connection:
        # NOTE: This can be run outside the main transaction, but requires its own commit
        connection.execute(text(sql), params)
        connection.commit()