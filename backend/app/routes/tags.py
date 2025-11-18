from flask import Blueprint, request, jsonify, current_app, make_response, g
from app.services.input_validatore import Validator, inputValidationExeption, validate_profile_update_data
from app.midlewares.auth_middleware import token_required, AuthRequiredException
from app.repositories.user import get_user_by_id, update_user_profile
from app.constants.tags import ALL_TAGS, CATEGORY_IDS

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