from flask import Blueprint, request, jsonify, current_app, make_response, g
from app.services.input_validatore import Validator, inputValidationExeption, validate_profile_update_data, validate_update_tags_data, validate_location_update
from app.midlewares.auth_middleware import token_required, AuthRequiredException
from app.repositories.user import get_user_by_id, update_user_profile, update_user_tags
from app.constants.tags import ALL_TAGS, CATEGORY_IDS
from app.repositories.location import update_or_insert_location
from app.services.file_handler import allowed_file, save_uploaded_file
from app.repositories.picture import add_new_picture, count_user_pictures
# from werkzeug.exceptions import RequestEntityTooLarge # For size limit


bp = Blueprint('profile', __name__)

@bp.route('/', methods=['PUT'])
@token_required
def method_name():
    # required fields for profile update
    try:
        REQUIRED_FIELDS = ['username','first_name', 'last_name', 'biography', 'gender', 'sexual_preferences', 'birthdate']
        data = Validator(required_fields=REQUIRED_FIELDS).validate_json(request.json)
        print(f"this is the user from g: {g.user}")
        user = get_user_by_id(g.user['id'])
        
        if not user:
            raise AuthRequiredException("User not found in database.", status_code=401)
        if not user.get('is_verified'):
            raise AuthRequiredException("Account not verified.", status_code=403)
        # validate profile update data
        data = validate_profile_update_data(data, current_user_id=user['id'])
        update_user_profile(user['id'], data)
        return jsonify({"message": "Profile updated successfully."}), 200
    except inputValidationExeption as e:
        print(f"Input validation error during profile update: {e}")
        return jsonify({
            "error": e.args[0], 
            "details": e.errors
        }), e.status_code
    except AuthRequiredException as e:
        print(f"Authentication error during profile update: {e.args[0]}")
        return jsonify({"error": e.args[0]}), e.status_code
    except Exception as e:
        print(f"Unexpected error during profile update: {e}")
        return jsonify({"error": "An unexpected server error occurred."}), 500



#update_user_tags
@bp.route('/tags/update-user-tags', methods=['PUT'])
@token_required
def update_tags():
    try:
        data = Validator(required_fields=['tags']).validate_json(request.json)
        tags = data.get('tags', [])
        if not isinstance(tags, list):
            raise inputValidationExeption("Tags must be provided as a list.", status_code=422)
        data = validate_update_tags_data(data)
        update_user_tags(g.user['id'], tags)
        return jsonify({"message": "User tags updated successfully."}), 200
    except inputValidationExeption as e:
        print(f"Input validation error during tag update: {e}")
        return jsonify({
            "error": e.args[0], 
            "details": e.errors
        }), e.status_code
    except AuthRequiredException as e:
        print(f"Authentication error during tag update: {e.args[0]}")
        return jsonify({"error": e.args[0]}), e.status_code
    except Exception as e:
        print(f"Unexpected error during tag update: {e}")
        return jsonify({"error": "An unexpected server error occurred."}), 500
    
#update user location
@bp.route('/location', methods=['PUT'])
@token_required
def update_location():
    user_id = g.user['id']
    try:
        # data = Validator(required_fields=['is_gps_enabled']).validate_json(request.json)
        data = validate_location_update(request.json)
        # Call the repository function to update user location
        update_or_insert_location(user_id, data)
        return jsonify({"message": "User location updated successfully."}), 200
    except inputValidationExeption as e:
        print(f"Input validation error during location update: {e}")
        return jsonify({
            "error": e.args[0], 
            "details": e.errors
        }), e.status_code
    except AuthRequiredException as e:
        print(f"Authentication error during location update: {e.args[0]}")
        return jsonify({"error": e.args[0]}), e.status_code
    except Exception as e:
        print(f"Unexpected error during location update: {e}")
        return jsonify({"error": "An unexpected server error occurred."}), 500
    
    
@bp.route('/pictures', methods=['POST'])
@token_required
def upload_profile_picture():
    user_id = g.user['id']
    
    max_pictures = current_app.config['MAX_USER_PICTURES']
    current_count = count_user_pictures(user_id)

    if current_count >= max_pictures:
        return jsonify({
            "error": f"You have exceeded the maximum limit of {max_pictures} pictures."
        }), 403 # Use 403 Forbidden for business logic violation

    if 'file' not in request.files:
        return jsonify({"error": "Missing file part in the request."}), 400
    
    file = request.files['file']
    try:
        file_path = save_uploaded_file(file, user_id)
        new_pic_id = add_new_picture(user_id, file_path, is_profile_picture=False)
        
        return jsonify({
            "message": "Picture uploaded successfully.",
            "picture_id": new_pic_id,
            "file_path": file_path
        }), 201
    except ValueError:
        return jsonify({"error": "Uploaded file exceeds the maximum allowed size."}), 413
    except AuthRequiredException as e:
        print(f"Authentication error during picture upload: {e.args[0]}")
        return jsonify({"error": e.args[0]}), e.status_code
    except Exception as e:
        print(f"Unexpected error during picture upload: {e}")
        return jsonify({"error": "An unexpected server error occurred."}), 500
