import os
from flask import current_app
from werkzeug.utils import secure_filename
import time


def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
        
def save_uploaded_file(file, user_id):
    if not file or not file.filename or not allowed_file(file.filename):
        raise ValueError("Invalid file or file type not allowed.")
    
    extension = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = f"user_{user_id}_{int(time.time())}.{extension}"
    secure_name = secure_filename(unique_filename)
    
    #create user specifique foalder is not exists
    user_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
    os.makedirs(user_dir, exist_ok=True)
    
    file_path = os.path.join(user_dir, secure_name)
    file.save(file_path)
    
    return os.path.join(str(user_id), secure_name)  # Return relative path for storage in DB