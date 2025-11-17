# custom exeption for email verification errors
class EmailVerificationException(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code
    def __str__(self):
        return f"EmailVerificationException: {self.args[0]} (status code: {self.status_code})"
    
# Example usage:
# raise EmailVerificationException("Invalid or expired token.", status_code=401)