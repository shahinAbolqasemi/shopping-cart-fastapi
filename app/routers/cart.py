from fastapi import APIRouter, Depends
from app.dependencies import get_current_active_user, get_cart_items_by_username
from app.models import User

router = APIRouter()


@router.get("/")
async def cart_list_items(
        cart_items: list = Depends(get_cart_items_by_username)
):
    return {
        "result": "OK",
        "response": cart_items
    }


@router.post("/")
async def cart_add_item(user: User = Depends(get_current_active_user)):
    return {"message": "Cart API Add"}


@router.delete("/")
async def cart_delete(user: User = Depends(get_current_active_user)):
    return {"message": "Cart API Delete"}


@router.delete("/{id}")
async def cart_delete_item(cart_id: int, user: User = Depends(get_current_active_user)):
    return {"message": "Cart API Delete Item"}


@router.put("/")
async def cart_update(user: User = Depends(get_current_active_user)):
    return {"message": "Cart API Update Whole Cart"}


@router.patch("/")
async def cart_partial_update(user: User = Depends(get_current_active_user)):
    return {"message": "Cart API Update"}
