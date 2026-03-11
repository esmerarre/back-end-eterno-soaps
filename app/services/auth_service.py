import os
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash


# Secret used to sign JWTs. Set this in .env for real deployments.
SECRET_KEY = os.getenv("ADMIN_JWT_SECRET", "change-me-in-production")
# HMAC-SHA256 signing algorithm.
ALGORITHM = "HS256"
# Default token lifetime (minutes).
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# pwdlib PasswordHash handles password hashing/verification.
# .recommended() picks the best available algorithm — Argon2 in this case,
# since pwdlib[argon2] is installed. Argon2 is the current gold standard
pwd_context = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Compare user-entered password against stored hash.
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    # One-way hash used for storage in the DB.
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    # Start with provided claims (e.g., {"sub": username}).
    to_encode = data.copy()
    # Compute expiration timestamp.
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    # Add exp claim so token automatically expires.
    to_encode.update({"exp": expire})
    # Sign and encode JWT.
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    try:
        # Decode + validate signature/expiry.
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        # Invalid, malformed, or expired token.
        return None
