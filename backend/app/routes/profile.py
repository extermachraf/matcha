from flask import Blueprint, request, jsonify, current_app, make_response
from app.services.input_validatore import Validator, inputValidationExeption
from app.midlewares.auth_middleware import token_required, AuthRequiredException


bp = Blueprint('profile', __name__)

@bp.route('/', methods=['PUT'])
@token_required
def method_name():
    # required fields for profile update
    try:
        REQUIRED_FIELDS = ['first_name', 'last_name', 'biography', 'gender', 'sexual_preferences', ]
        return jsonify({"message": "Profile updated successfully."}), 200
    except AuthRequiredException as e:
        print(f"Authentication error during profile update: {e}")
        return jsonify({"error": e.args[0]}), e.status_code
    except Exception as e:
        print(f"Unexpected error during profile update: {e}")
        return jsonify({"error": "An unexpected server error occurred."}), 500
