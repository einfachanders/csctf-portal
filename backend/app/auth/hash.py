from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

async def verify_password_hash(hash: str, password: str) -> bool:
    """Checks wether a password matches the given argon2 hash

    Args:
        hash (str): hash to match
        password (str): password to verify

    Returns:
        bool
    """
    try:
        return ph.verify(hash, password)
    except VerifyMismatchError:
        return False
