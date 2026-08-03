import hashlib
import secrets

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def create_token():
    return secrets.token_urlsafe(32)