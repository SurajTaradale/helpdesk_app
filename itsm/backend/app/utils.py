import hashlib
import random
import string

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_random_password(length: int = 12) -> str:
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
