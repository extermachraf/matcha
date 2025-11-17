import jwt
from flask import current_app
from datetime import datetime, timedelta, timezone
from app.exeptions.token_exeption import TokenVerificationException


def generate_verification_token(user_id: int) -> str:
    """Generates a time-limited JWT for email verification."""
    # Get the JWT secret key from the application configuration
    
    jwt_secret = current_app.config.get('JWT_SECRET_KEY')
    print(f"this is the jwt secret key: {jwt_secret}")
    lifetime_seconds = current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 3600) # Default 1 hr

    # Define the token payload (claims)
    payload = {
        # 'sub' (subject): The user ID the token is about
        'sub': user_id, 
        # 'iat' (issued at): Timestamp of when the token was created
        'iat': datetime.now(timezone.utc),
        # 'exp' (expiration time): When the token expires (e.g., 1 hour from now)
        'exp': datetime.now(timezone.utc) + timedelta(seconds=lifetime_seconds),
        # 'type' (custom claim): Identifies the token's purpose
        'type': 'verify'
    }

    # Encode the payload into a JWT
    token = jwt.encode(
        payload,
        jwt_secret,
        algorithm='HS256' # Standard hashing algorithm
    )
    return token

def validate_jwt_token(token: str) -> dict:
    try:
        jwt_secret = current_app.config.get('JWT_SECRET_KEY')
        payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        if payload.get('type') != 'verify':
            raise TokenVerificationException("Invalid token type.", status_code=401)
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenVerificationException("Token has expired.", status_code=401)
    except jwt.InvalidTokenError:
        raise TokenVerificationException("Invalid token.", status_code=401)
    except Exception as e:
        raise TokenVerificationException(f"Token verification failed: {e}", status_code=400)