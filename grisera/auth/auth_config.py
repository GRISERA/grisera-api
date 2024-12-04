import os

KEYCLOAK_SERVER = os.environ.get("KEYCLOAK_SERVER") or "http://localhost:8090"
REALM = os.environ.get("REALM") or "grisera"
JWKS_URL = os.environ.get("JWKS_URL") or f"{KEYCLOAK_SERVER}/realms/{REALM}/protocol/openid-connect/certs"
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM") or "RS256"
CLIENT_ID = os.environ.get("CLIENT_ID") or "grisera"