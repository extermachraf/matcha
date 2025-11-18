import os
from dotenv import load_dotenv

# Load environment values from .env; the project will rely on a single
# canonical variable `DATABASE_URL` stored in .env (per user's request).
load_dotenv()


class Config:
    """Base configuration: rely only on `DATABASE_URL` from .env/environment."""
    BACKEND_HOST=os.environ.get('BACKEND_HOST')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # dtabase infos
    DATABASE_URL = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # jwt informations
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = 86400  # 24 hours
    
    #smtp informations
    RESEND_API_KEY = os.environ.get('RESEND_API_KEY')
    
    # file system storage configuration
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'user_uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit for uploaded files
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    # Picture Upload Limits
    MAX_USER_PICTURES = int(os.environ.get('MAX_USER_PICTURES', 5)) # Default to 5


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    # Add production-specific config here