from flask import Blueprint, request, jsonify, current_app, make_response
from app.services.input_validatore import Validator, inputValidationExeption, validate_registration_data, validate_email_format
from app.repositories.user import check_user_uniqueness, create_new_user, verify_user, get_user_by_email, update_user_password, update_user_last_seen
from app.services.password_handler import hash_password, verify_password
from app.services.jwt_handler import generate_verification_token, validate_jwt_token
from app.services.smtp_handler import send_verification_email, send_password_reset_email
from app.exeptions.token_exeption import TokenVerificationException
from app.exeptions.email_exeption import EmailVerificationException

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    # Define required fields for registration
    REQUIRED_FIELDS = ['username', 'email', 'password', 'first_name', 'last_name']
    #print in server side request recieved
    # Use the debugger to inspect the request context interactively
    try:
        # 1. validate data presence and basic format
        data = Validator(required_fields=REQUIRED_FIELDS).validate_json(request.json)
        data = validate_registration_data(request.json)
        
        #uniqueness check to be implemented here
        duplicates = check_user_uniqueness(data['username'], data['email'])
        if duplicates:
            error_details = {}
            if 'username' in duplicates:
                error_details['username'] = "Username already exists."
            if 'email' in duplicates:
                error_details['email'] = "Email already registered."
            raise inputValidationExeption("Uniqueness validation failed.", errors=error_details, status_code=409)
        # hashing password before storing
        data['password'] = hash_password(data['password'])
        # Create the new user record
        new_user_id = create_new_user(data)
        # generate url tokens
        verification_url = f"{current_app.config.get('BACKEND_HOST')}/auth/verify-email?token={generate_verification_token(new_user_id)}"
        if send_verification_email(data['email'], verification_url):
            return jsonify({"message": "Registration successful. Verification email sent."}), 201
        else:
            # Handle failure gracefully (e.g., log error, prompt user to retry)
            return jsonify({"error": "Registration failed: Could not send verification email."}), 500
    except inputValidationExeption as e:
        # Return structured error response
        return jsonify({
            "error": e.args[0], 
            "details": e.errors
        }), e.status_code
    except Exception as e:
        # Catch unexpected server-side errors
        print(f"Unexpected error during registration: {e}")
        return jsonify({"error": "An unexpected server error occurred."}), 500
    
@bp.route('/verify-email', methods=['GET'])
def verify_email():
    try:
        token = request.args.get('token', None)
        if not token:
            raise EmailVerificationException("Missing verification token.", status_code=400)
        # Validate the token and extract payload
        payaload = validate_jwt_token(token)
        
        # update user record to set email as verified
        verify_user(payaload['sub'])
        return jsonify({"message": "Email successfully verified."}), 200
        
    except EmailVerificationException as e:
        print(f"Email verification error: {e}")
        return jsonify({"error": e.args[0]}), e.status_code
    except TokenVerificationException as e:
        print(f"Token verification error: {e}")
        return jsonify({"error": e.args[0]}), e.status_code
    except Exception as e:
        print(f"Unexpected error during email verification: {e}")
        return jsonify({"error": "An unexpected server error occurred."}), 500
    
@bp.route('/password/reset-request', methods=['POST'])
def password_reset_request():
    try:
        REQUIRED_FIELDS = ['email']
        print("we are here")
        #validate json and presence of email field
        data = Validator(required_fields=REQUIRED_FIELDS).validate_json(request.json)
        # take email from request body
        email = validate_email_format(request.json.get('email', None))
        user = get_user_by_email(email)
        if not user:
            raise inputValidationExeption("No user found with the provided email.", status_code=404)
        # generate password reset token
        reset_url = f"{current_app.config.get('FRONTEND_HOST')}/auth/reset-password?token={generate_verification_token(user['id'])}"
        
        print(f"this is the reset url: {reset_url}")
        # send password reset email
        if send_password_reset_email(email, reset_url):
            # TODO: front end should extract token from url and provide new password form
            return jsonify({"message": "Password reset email sent."}), 200
        else:
            print("Failed to send password reset email.")
            raise EmailVerificationException("Failed to send password reset email.", status_code=500)
        
    except EmailVerificationException as e:
        print(f"Email sending error during password reset request: {e}")
        return jsonify({"error": e.args[0]}), e.status_code
    except inputValidationExeption as e:
        print(f"Input validation error during password reset request: {e}")
        return jsonify({
            "error": e.args[0], 
            "details": e.errors
        }), e.status_code
    except Exception as e:
        print(f"Unexpected error during password reset request: {e}")
        return jsonify({"error": "An unexpected server error occurred."}), 500
    
@bp.route('/password/reset', methods=['POST'])
def reset_password():
    try:
        REQUIRED_FIELDS = ['token', 'new_password']
        #validate json and presence of required fields
        data = Validator(required_fields=REQUIRED_FIELDS).validate_json(request.json)
        token = Validator().validate_token(request.json.get('token', None))
        new_password = request.json.get('new_password', None)
        # TODO : add more password strength validations here
        if not new_password or len(new_password) < 8:
            raise inputValidationExeption("New password must be at least 8 characters long.", status_code=422)
        # validate token and extract payload
        payload = validate_jwt_token(token)
        user_id = payload['sub']
        # hash the new password
        hashed_password = hash_password(new_password)
        # update user's password in the database
        update_user_password(user_id, hashed_password)
        return jsonify({"message": "Password successfully reset."}), 200
    except TokenVerificationException as e:
        print(f"Token verification error during password reset: {e}")
        return jsonify({"error": e.args[0]}), e.status_code
    except inputValidationExeption as e:
        print(f"Input validation error during password reset: {e}")
        return jsonify({
            "error": e.args[0], 
            "details": e.errors
        }), e.status_code
    except Exception as e:
        print(f"Unexpected error during password reset: {e}")
        return jsonify({"error": "An unexpected server error occurred."}), 500
    
@bp.route('/login', methods=['POST'])
def login():
    try:
        REQUIRED_FIELDS = ['email', 'password']
        data = Validator(required_fields=REQUIRED_FIELDS).validate_json(request.json)
        user = get_user_by_email(data['email'])
        if not user:
            raise inputValidationExeption("No user found with the provided email.", status_code=404)
        if not user['is_verified']:
            raise inputValidationExeption("Email not verified. Please verify your email before logging in.", status_code=403)
        print(f"this is our pretty user: {user}")
        if not verify_password(data['password'], user['password_hash']):
            raise inputValidationExeption("Incorrect password.", status_code=401)
        #generate token
        token = generate_verification_token(user['id'])
        # update last seen
        update_user_last_seen(user['id'])
        
        response_data = {
            "message": "Login successful.",
            "user": {
                "id": user['id'],
                "username": user['username'],
                "email": user['email'],
                "first_name": user['first_name'],
                "last_name": user['last_name'],
                "fame_rating": user['fame_rating'],
                # add other non-sensitive fields as needed
            }
        }
        
        response = make_response(jsonify(response_data), 200)
        response.set_cookie('auth_token', token, httponly=True, secure=True, samesite='Lax')
        
        return response
    except inputValidationExeption as e:
        print(f"Input validation error during login: {e}")
        return jsonify({
            "error": e.args[0], 
            "details": e.errors
        }), e.status_code
    except Exception as e:
        print(f"Unexpected error during login: {e}")
        return jsonify({"error": "An unexpected server error occurred."}), 500
    
@bp.route('/logout', methods=['POST'])
def logout():
    try:
        response = make_response(jsonify({"message": "Logout successful."}), 200)
        response.set_cookie('auth_token', '', expires=0, httponly=True, secure=True, samesite='Lax')
        return response
    except Exception as e:
        print(f"Unexpected error during logout: {e}")
        return jsonify({"error": "An unexpected server error occurred."}), 500