# app/midlewares/auth_middleware.py

from functools import wraps
from flask import request, jsonify, g
import jwt
from app.services.jwt_handler import validate_jwt_token
from app.repositories.user import get_user_by_id

class AuthRequiredException(Exception):
    """Custom exception raised for all authentication/authorization failures."""
    def __init__(self, message, status_code=401):
        super().__init__(message)
        self.status_code = status_code

def token_required(f):
    """
    Decorator that checks for a valid JWT in the cookie or Authorization header.
    If valid, it loads the user object into flask.g.user.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 1. Token Retrieval (Priority: HTTP-Only Cookie)
        token = request.cookies.get('auth_token')
        print("Auth Token from Cookie:", token)
        if not token:
            # 2. Fallback: Authorization Header (Bearer Token)
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({"error": "Authentication token is missing."}), 401

        try:
            # 3. Decode and Validate Token
            # This checks signature, expiration, and type='access'
            token_data = validate_jwt_token(token) 
            user_id = token_data['sub']
            
            # 4. Load User Identity from DB
            user = get_user_by_id(user_id) 
            
            if not user:
                # If the token is valid but the user was deleted
                raise AuthRequiredException("User not found in database.", status_code=401)
                
            if not user.get('is_verified'):
                # MANDATORY PROJECT CHECK: User must be verified
                raise AuthRequiredException("Account not verified.", status_code=403)

        except jwt.ExpiredSignatureError:
            # delet token from cookies if exists
            response = jsonify({"error": "Authentication token has expired."})
            response.set_cookie('auth_token', '', expires=0, httponly=True, secure=True, samesite='Lax')
            return response, 401
        
        except jwt.InvalidTokenError:
            # Catches signature failure or incorrect token type
            return jsonify({"error": "Invalid or tampered authentication token."}), 401
        
        except AuthRequiredException as e:
            # Catches exceptions raised inside the try block (e.g., 403 status)
            return jsonify({"error": e.args[0]}), e.status_code
            
        except Exception as e:
            # Log unexpected server errors during token processing
            print(f"Token Processing Unexpected Error: {e}")
            return jsonify({"error": "Authentication failed due to server error."}), 500

        # 5. Pass User Data to the Route
        g.user = user
        
        # Execute the original route function
        return f(*args, **kwargs)

    return decorated