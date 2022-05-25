from fastapi import APIRouter, Depends, status, Path

from app.dependencies import (
    get_current_active_user,
    get_cart_items_by_username,
    add_item_to_cart,
    delete_item_from_cart,
    delete_cart_items,
)
from app.models import User

router = APIRouter()


@router.get("/")
async def cart_list_items(cart_items: list = Depends(get_cart_items_by_username)):
    return {
        "result": "OK",
        "response": cart_items
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def cart_add_item(user: User = Depends(get_current_active_user), product: dict = Depends(add_item_to_cart)):
    return {"result": "OK", "response": product}


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(delete_cart_items)]
)
async def cart_delete_all_items(user: User = Depends(get_current_active_user)):
    return {"result": "OK", "response": "All items deleted"}


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(delete_item_from_cart)]
)
async def cart_delete_item(product_id: int = Path(...), user: User = Depends(get_current_active_user)):
    return {"result": "OK", "response": f"Item {product_id} deleted"}


@router.put("/")
async def cart_update(user: User = Depends(get_current_active_user)):
    return {"result": "OK", "message": "Cart API Update Whole Cart. Not implemented yet"}


@router.patch("/")
async def cart_partial_update(user: User = Depends(get_current_active_user)):
    return {"result": "OK", "message": "Cart API Update. Not implemented yet"}
