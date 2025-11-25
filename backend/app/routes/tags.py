from flask import Blueprint, request, jsonify, current_app, make_response, g
from app.services.input_validatore import Validator, inputValidationExeption, validate_profile_update_data
from app.midlewares.auth_middleware import token_required, AuthRequiredException
from app.repositories.user import get_user_by_id, update_user_profile
from app.constants.tags import ALL_TAGS, CATEGORY_IDS
from app.repositories.tags import get_user_tags_by_id

bp = Blueprint('tags', __name__)

@bp.route('/all-tags', methods=['GET'])
def get_all_tags():
    """Returns all available tags grouped by category name."""
    
    # Reverse the CATEGORY_IDS map for easy lookup: {id: name}
    category_names = {v: k for k, v in CATEGORY_IDS.items()}
    
    # Initialize the final structured list
    structured_tags = {}
    for name in CATEGORY_IDS.keys():
        structured_tags[name] = []
        
    # Group tags by category name
    for tag_name, category_id in ALL_TAGS.items():
        category_name = category_names.get(category_id, "Other")
        structured_tags[category_name].append(tag_name)
        
    return jsonify(structured_tags), 200


@bp.route('/user-tags/<int:id>', methods=['GET'])
@token_required
def get_user_tags(id):
    """Returns the tags associated with the authenticated user."""
    if not id:
        return jsonify({"error": "User ID is required"}), 400
    try:
        user_tags = get_user_tags_by_id(id)
        return jsonify({"tags": user_tags}), 200
    except Exception as e:
        current_app.logger.error(f"Error retrieving user tags for user_id {id}: {e}")
        return jsonify({"error": "Failed to retrieve user tags"}), 500
    # call get user tags by id from repository