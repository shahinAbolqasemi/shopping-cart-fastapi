from fastapi import status, Depends, HTTPException, Path
from app.db import get_user
from jose import jwt, JWTError
from app.models import TokenData, User
from app.security.security import oauth2_scheme
from app.config import get_settings
from app.db import get_cart_item
import aiohttp

settings = get_settings()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_cart_items_by_username(user: User = Depends(get_current_active_user)):
    cart_items_id = get_cart_item(user.username)

    async with aiohttp.ClientSession() as session:
        async with session.get(
                "https://fakestoreapi.com/products"
        ) as response:
            results = await response.json()
            cart_items = []
            for item_id, quantity in cart_items_id:
                for product in results:
                    if item_id == product["id"]:
                        product["quantity"] = quantity
                        cart_items.append(product)
                        break
    return cart_items
