from app.repositories.connection import get_db_engine
from sqlalchemy import text


def check_user_uniqueness(username, email):
    """
    Checks the 'users' table to see if the username or email already exists.

    Returns:
        A list of column names that are duplicates (e.g., ['username', 'email'])
    """
    engine = get_db_engine()
    
    # 1. Manual SQL Query
    sql = """
        SELECT
            username, email
        FROM
            users
        WHERE
            username = :username_param OR email = :email_param
        LIMIT 1;
    """
    
    # 2. Parameterization (Crucial for security)
    params = {
        'username_param': username, 
        'email_param': email
    }
    
    with engine.connect() as connection:
        result = connection.execute(text(sql), params).fetchone()
    
    # 3. Process the Result
    if result is None:
        return [] # No duplicates found
        
    duplicates = []
    
    # The result contains the username and email found in the database
    db_username = result[0]
    db_email = result[1]
    
    # Check which input matched the database record
    if db_username == username:
        duplicates.append('username')
    if db_email == email:
        duplicates.append('email')
        
    return duplicates


def create_new_user(user_data: dict) -> int:
    """
    Inserts the core user record into the 'users' table and returns the new ID.
    
    Args:
        user_data: Dictionary containing validated user info (username, email, etc.).
        password_hash: The securely hashed password string.
        
    Returns:
        The newly created user's ID (int).
    """
    engine = get_db_engine()
    
    # 1. Manual SQL INSERT Statement
    # We use RETURNING id to get the PostgreSQL-generated ID in the same query.
    sql = """
        INSERT INTO users (
            username, email, password_hash, first_name, last_name
        )
        VALUES (
            :username, :email, :p_hash, :first_name, :last_name
        )
        RETURNING id;
    """
    
    # 2. Parameter Dictionary
    # This maps the :placeholders in the SQL query to the Python variables.
    params = {
        'username': user_data['username'],
        'email': user_data['email'],
        'p_hash': user_data['password'],
        'first_name': user_data['first_name'],
        'last_name': user_data['last_name'],
    }
    
    try:
        with engine.connect() as connection:
            # Execute the query securely using parameterization
            result = connection.execute(text(sql), params)
            
            # Commit the transaction to make the new record permanent
            connection.commit()
            
            # Retrieve the ID returned by the RETURNING clause
            new_user_id = result.scalar_one()
            
            return new_user_id

    except Exception as e:
        # In a real app, you'd log the error here.
        raise Exception(f"Database insertion failed: {e}")
    
    
def verify_user(user_id: int):
    """
    Updates the user's record to set email as verified.
    
    Args:
        id: The user's ID to verify.
    """
    engine = get_db_engine()
    
    sql = """
        UPDATE users
        SET is_verified = TRUE
        WHERE id = :user_id;
    """
    
    params = {
        'user_id': user_id
    }
    
    try:
        with engine.connect() as connection:
            connection.execute(text(sql), params)
            connection.commit()
    except Exception as e:
        raise Exception(f"Failed to set is verified to true inside database: {e}")
    
    
def get_user_by_email(email: str) -> dict | None:
    """
    Retrieves a user record by email.
    
    Args:
        email: The email address to search for.
        
    Returns:
        A dictionary of the user record if found, else None.
    """
    engine = get_db_engine()
    
    sql = """
        SELECT * FROM users
        WHERE email = :email_param
        LIMIT 1;
    """
    
    params = {
        'email_param': email
    }
    
    with engine.connect() as connection:
        result = connection.execute(text(sql), params).fetchone()
        
    if result is None:
        return None
    
    return dict(result._mapping)


def update_user_password(user_id: int, new_password_hash: str):
    """
    Updates the user's password hash in the database.
    
    Args:
        user_id: The ID of the user whose password is to be updated.
        new_password_hash: The new hashed password.
    """
    engine = get_db_engine()
    
    sql = """
        UPDATE users
        SET password_hash = :new_hash
        WHERE id = :user_id;
    """
    
    params = {
        'new_hash': new_password_hash,
        'user_id': user_id
    }
    
    try:
        with engine.connect() as connection:
            connection.execute(text(sql), params)
            connection.commit()
    except Exception as e:
        raise Exception(f"Failed to update user password in database: {e}")
    
def update_user_last_seen(user_id: int):
    """
    Updates the user's last seen timestamp in the database.
    
    Args:
        user_id: The ID of the user whose last seen is to be updated.
    """
    engine = get_db_engine()
    
    sql = """
        UPDATE users
        SET last_seen = NOW()
        WHERE id = :user_id;
    """
    
    params = {
        'user_id': user_id
    }
    
    try:
        with engine.connect() as connection:
            connection.execute(text(sql), params)
            connection.commit()
    except Exception as e:
        raise Exception(f"Failed to update user last seen in database: {e}")
    
def get_user_by_id(user_id: int) -> dict | None:
    """
    Retrieves a user record by user ID.
    
    Args:
        user_id: The ID of the user to retrieve.
        
    Returns:
        A dictionary of the user record if found, else None.
    """
    engine = get_db_engine()
    
    sql = """
        SELECT * FROM users
        WHERE id = :user_id_param
        LIMIT 1;
    """
    
    params = {
        'user_id_param': user_id
    }
    
    with engine.connect() as connection:
        result = connection.execute(text(sql), params).fetchone()
        
    if result is None:
        return None
    
    return dict(result._mapping)

def update_user_profile(user_id: int, data: dict):
    """
    Updates multiple user fields in the 'users' table using manual SQL.
    """
    engine = get_db_engine()
    
    # Dynamically build the SET clause for the UPDATE query
    # This prevents errors if not all fields are passed
    set_clauses = []
    params = {'id': user_id}
    
    # Map input keys to column names
    valid_fields = [
        'username', 'first_name', 'last_name', 'biography', 
        'gender', 'sexual_preferences', 'birthdate'
    ]
    
    for key, value in data.items() :
        if key in valid_fields:
            # Add clause: 'column_name = :placeholder'
            set_clauses.append(f"{key} = :{key}")
            params[key] = value
            
    if not set_clauses:
        # Prevent running an empty update query
        return False

    sql = f"""
        UPDATE users
        SET {', '.join(set_clauses)}
        WHERE id = :id;
    """
    
    try:
        with engine.connect() as connection:
            connection.execute(text(sql), params)
            connection.commit()
            return True
    except Exception as e:
        # PostgreSQL integrity error (e.g., unique constraint violation for username/email)
        # You would catch specific psycopg2 errors here for a unique key violation.
        raise Exception(f"Database update failed: {e}")
    
# check username uniquenes_excluding a user id
def check_username_uniqueness_exept_id(username: str, user_id: int) -> bool:
    """
    Checks if the given username is unique, excluding the specified user ID.
    
    Args:
        username: The username to check for uniqueness.
        user_id: The user ID to exclude from the check.
    Returns:
        True if the username is unique, False if it already exists for another user.
    """
    engine = get_db_engine()
    
    sql = """
        SELECT 1 FROM users
        WHERE username = :username_param AND id != :user_id_param
        LIMIT 1;
    """
    
    params = {
        'username_param': username,
        'user_id_param': user_id
    }
    
    with engine.connect() as connection:
        result = connection.execute(text(sql), params).fetchone()
        
    return result is None  # True if unique, False if duplicate found
