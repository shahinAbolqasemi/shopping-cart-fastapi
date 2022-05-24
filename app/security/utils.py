from fastapi.security import OAuth2PasswordBearer
from fastapi import Request, Query, status, HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from typing import Union, Optional


class OAuth2PasswordBearerCustom(OAuth2PasswordBearer):
    async def __call__(self, request: Request, token: Optional[str] = Query('')) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            authorization = token
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param
