import time
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

import jwt

from grisera.auth.auth_config import JWT_ALGORITHM, JWKS_URL, ISSUER
import requests


def get_jwks():
    response = requests.get(JWKS_URL)
    response.raise_for_status()
    return response.json()["keys"]


def get_key_by_kid(kid: str):
    jwks = get_jwks()
    for key in jwks:
        if key["kid"] == kid:
            return key
    raise ValueError("Key not found")


def verify_jwt(jwtoken: str) -> bool:
    try:
        payload = decode_jwt(jwtoken)
        return payload is not None
    except Exception as e:
        return False


def construct_pem_key(key):
    if key["kty"] != "RSA":
        raise ValueError("Only RSA keys are supported")

    exponent = int.from_bytes(jwt.utils.base64url_decode(key["e"]), "big")
    modulus = int.from_bytes(jwt.utils.base64url_decode(key["n"]), "big")

    public_key = rsa.RSAPublicNumbers(exponent, modulus).public_key()
    return public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)


def decode_jwt(token: str) -> dict:
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        if not kid:
            raise ValueError("Token header missing 'kid'")

        key = get_key_by_kid(kid)

        public_key = construct_pem_key(key)

        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=[JWT_ALGORITHM],
            verify_iss=ISSUER is not None,
            issuer=ISSUER,
        )

        if decoded_token["exp"] < time.time():
            raise ValueError("Token has expired")

        return decoded_token
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None
