import time
import jwt
from grisera.auth.auth_config import JWT_SECRET, JWT_ALGORITHM

def verify_jwt(jwtoken: str) -> bool:
    is_token_valid: bool = False

    try:
        payload = decodeJWT(jwtoken)
    except:
        payload = None
    if payload:
        is_token_valid = True
    return is_token_valid

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except Exception as e:
        return {}