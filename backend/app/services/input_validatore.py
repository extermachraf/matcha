
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
