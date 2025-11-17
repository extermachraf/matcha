# custom exception for token verification errors
class TokenVerificationException(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code
    def __str__(self):
        return f"TokenVerificationException: {self.args[0]} (status code: {self.status_code})"