import os

JWT_SECRET = os.environ.get("JWT_SECRET") or "jwtsecret"
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM") or "HS256"
