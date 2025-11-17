from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    default="bcrypt",
    # Set the cost factor for bcrypt. Higher is slower but more secure.
    # A value of 12 is a good default balance for modern CPUs.
    bcrypt__rounds=12
)

def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plaintext password against the stored hash."""
    return pwd_context.verify(password, password_hash)