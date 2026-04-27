import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_database
from app.models.item import ItemCreate, ItemResponse, ItemUpdate, Item

logger = logging.getLogger(__name__)
router = APIRouter()



@router.get("/items", response_model=list[ItemResponse])
async def list_items(db: AsyncSession = Depends(get_database)):
    """List all items."""
    logger.info("Listing all items", extra={"endpint": "/items"})
    result = await db.execute(select(Item))
    return result.scalars().all()    


# @router.post("/items", response_model=ItemResponse, status_code=201)
# async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_database)):
#     """Create a new item."""
#     global next_id
    
#     new_item = ItemResponse(
#         id=next_id,
#         name=item.name,
#         description=item.description,
#         price=item.price,
#     )
#     items_db.append(new_item)
#     next_id += 1

#     logger.info(f"Created item: {new_item}")
#     return new_item
