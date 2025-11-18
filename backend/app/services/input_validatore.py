import re
from datetime import datetime, date
from app.repositories.user import check_username_uniqueness_exept_id

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