from typing import Optional

import jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, SecurityScopes

from app.core.config import settings


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        """Returns HTTP 403"""
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)


class UnauthenticatedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication")


async def get_auth0_decoded_token(
    security_scopes: SecurityScopes, token: Optional[HTTPAuthorizationCredentials]
):
    jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    jwks_client = jwt.PyJWKClient(jwks_url)
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token.credentials).key
    except jwt.exceptions.PyJWKClientError as error:
        raise UnauthorizedException(str(error))
    except jwt.exceptions.DecodeError as error:
        raise UnauthorizedException(str(error))
    try:
        payload = jwt.decode(
            token.credentials,
            signing_key,
            algorithms=settings.AUTH0_ALGORITHMS,
            audience=settings.AUTH0_API_AUDIENCE,
            issuer=settings.AUTH0_ISSUER,
        )
        return payload
    except jwt.JWTError as error:
        raise UnauthorizedException(str(error))
