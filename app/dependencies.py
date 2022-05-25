import aiohttp
from fastapi import status, Depends, HTTPException, Path
from jose import jwt, JWTError

from app.config import get_settings
from app.db import (
    get_user,
    get_cart_item,
    add_to_cart,
    get_cart_by_username,
    remove_from_cart,
    remove_cart_items
)
from app.models import TokenData, User, CartItem
from app.security.security import oauth2_scheme

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


async def get_cart(user: User = Depends(get_current_active_user)):
    return get_cart_by_username(user.username)


async def add_item_to_cart(product_id: CartItem, cart: dict = Depends(get_cart)):
    add_to_cart(product_id.product_id, cart["id"])


async def delete_item_from_cart(product_id: int = Path(...), cart: dict = Depends(get_cart)):
    if not remove_from_cart(product_id, cart["id"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The product is not in the cart"
        )


async def delete_cart_items(cart: dict = Depends(get_cart)):
    if not remove_cart_items(cart["id"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The cart is empty"
        )
