import re
from datetime import datetime, date
from app.repositories.user import check_username_uniqueness_exept_id
from app.constants.tags import ALL_TAGS, CATEGORY_IDS

class inputValidationExeption(Exception):
    # custom exception for input validation errors
    def __init__(self, message, errors=None, status_code=400):
        super().__init__(message)
        self.errors = errors if errors is not None else {}
        self.status_code = status_code
        
# validator class for 
class Validator:
    def __init__(self, required_fields=None, request=None):
        self.required_fields = required_fields if required_fields is not None else []
        self.errors = {}
        self.request = request
    def validate_json(self ,request):
        try:
            
            # if not request.is_Json:
            #     raise inputValidationExeption("Content-Type must be 'application/json'", status_code=415)
            data = request
            print(f"this is the request data: {data}")
            if data is None:
                raise inputValidationExeption("invalid json format or empty body", status_code=400)
            for field in self.required_fields:
                if field not in data or data.get(field) is None or str(data.get(field)).strip() == "":
                    self.errors[field] = f"the field '{field}' is required and cannot be empty."
            if self.errors:
                raise inputValidationExeption("input validation failed", errors=self.errors, status_code=422)
            return data
        except inputValidationExeption:
            raise
        except Exception as e:
            raise inputValidationExeption(f"failed to parse request data {e}", status_code=400)
    def validate_token(self, token):
        if not token or not isinstance(token, str) or token.strip() == "":
            raise inputValidationExeption("Invalid or missing token.", status_code=400)
        return token.strip()
    
    # Example usage function for complex validation (e.g., email format)
def validate_registration_data(data):
    """Performs complex, semantic checks on registration data."""
    errors = {}
    
    # Example: Check email format
    if 'email' in data and '@' not in data['email']:
        errors['email'] = "Invalid email format."
        
    # Example: Check password length
    if 'password' in data and len(data['password']) < 8:
        errors['password'] = "Password must be at least 8 characters long."
        
    # Example: Check for valid name characters (a custom check)
    if 'first_name' in data and not data['first_name'].isalpha():
        errors['first_name'] = "First name must contain only letters."

    # TODO: must implement check for common words in passwords
    
    if errors:
        raise inputValidationExeption("Semantic validation failed.", errors=errors)
        
    return data

def validate_email_format(email: str) -> str:
    """Validates the format of an email address."""
    if not email or '@' not in email:
        raise inputValidationExeption("Invalid email format.", status_code=422)
    return email.strip().lower()



def validate_profile_update_data(data, current_user_id):
    """
    Performs complex, semantic checks on profile update data.
    Requires current_user_id to exclude the current user from uniqueness checks.
    """
    errors = {}
    
    # 1. Check Birthdate Format and Age (MANDATORY REQUIREMENT)
    if 'birthdate' in data:
        try:
            # Assumes birthdate is sent as YYYY-MM-DD
            birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d').date()
            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            
            # Require minimum age (e.g., 18)
            if age < 18 or age > 100:
                errors['birthdate'] = "User must be between 18 and 100 years old."
        except ValueError:
            errors['birthdate'] = "Invalid date format. Use YYYY-MM-DD."

    # 2. Check Gender/Sexual Preferences
    VALID_GENDERS = ['male', 'female', 'non-binary']
    VALID_PREFS = ['male', 'female', 'both']
    
    if 'gender' in data and data['gender'].lower() not in VALID_GENDERS:
        errors['gender'] = f"Gender must be one of: {', '.join(VALID_GENDERS)}."

    if 'sexual_preferences' in data and data['sexual_preferences'].lower() not in VALID_PREFS:
        errors['sexual_preferences'] = f"Preference must be one of: {', '.join(VALID_PREFS)}."
        
    # 3. Check for uniqueness username
    if check_username_uniqueness_exept_id(data.get('username'), current_user_id) is False:
        errors['username'] = "Username already in use by another account."

    if errors:
        raise inputValidationExeption("Profile data validation failed.", errors=errors)
        
    return data


def validate_update_tags_data(data):
    """
    Validates the tags data for updating user tags.
    Expects 'tags' to be a list of non-empty strings.
    
    """
    errors = {}
    
    if 'tags' not in data or not isinstance(data['tags'], list):
        errors['tags'] = "Tags must be provided as a list."
    else:
        for tag in data['tags']:
            if not isinstance(tag, str) or tag.strip() == "":
                errors['tags'] = "Each tag must be a non-empty string."
            elif tag not in ALL_TAGS:
                errors['tags'] = f"Invalid tag: '{tag}'."
    if errors:
        raise inputValidationExeption("Tags data validation failed.", errors=errors)
        
    return data


def validate_location_update(data):
    """
    Validates location data based on the presence of keys.
    """
    errors = {}
    
    # 1. Check for the mandatory 'is_gps_enabled' boolean
    if 'is_gps_enabled' not in data or not isinstance(data['is_gps_enabled'], bool):
        errors['is_gps_enabled'] = "Must provide a boolean value for 'is_gps_enabled'."
        
    # 2. If GPS is being enabled, Lat/Lon must be provided
    if data.get('is_gps_enabled') is True:
        if 'latitude' not in data or 'longitude' not in data:
            errors['coordinates'] = "Latitude and longitude are required when GPS is enabled."
        else:
            # Basic range check for numeric types
            try:
                lat = float(data['latitude'])
                lon = float(data['longitude'])
                if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                    errors['coordinates'] = "Invalid latitude/longitude range."
            except ValueError:
                errors['coordinates'] = "Latitude and longitude must be numeric."

    # 3. If GPS is disabled, we accept manual 'neighborhood' or approximate location.
    if data.get('is_gps_enabled') is False and 'neighborhood' in data:
        if not isinstance(data['neighborhood'], str) or len(data['neighborhood']) < 2:
            errors['neighborhood'] = "Neighborhood must be a valid string."
            
    if errors:
        raise inputValidationExeption("Location validation failed.", errors=errors)
        
    return data