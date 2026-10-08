from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import jwt
import os

load_dotenv()

secret = os.getenv("JWT_SECRET")


def encode_access_JWT(
    payload: dict,
    expires_in_minutes: int = 15
) -> str:
    token_payload = payload.copy()

    expiration = datetime.now(timezone.utc) + timedelta(
        minutes=expires_in_minutes
    )

    token_payload.update({
        "exp": expiration
    })

    return jwt.encode(
        token_payload,
        secret,
        algorithm="HS256"
    )


def decode_access_JWT(encoded_token: str) -> dict:
    try:
        return jwt.decode(
            encoded_token,
            secret,
            algorithms=["HS256"]
        )

    except jwt.ExpiredSignatureError:
        return {"error": "Access Token expired"}

    except jwt.InvalidTokenError:
        return {"error": "Invalid Token"}