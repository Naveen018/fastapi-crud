from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date, datetime
from bson import ObjectId
from ..models import Item, ItemCreate
from app.database import get_collection, object_id_to_str

router = APIRouter()
items_collection = get_collection("items")

@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    item_dict = item.dict()
    item_dict["insert_date"] = datetime.utcnow()
    if "expiry_date" in item_dict:
        item_dict["expiry_date"] = datetime.combine(item_dict["expiry_date"], datetime.min.time())
    new_item = await items_collection.insert_one(item_dict)
    created_item = await items_collection.find_one({"_id": new_item.inserted_id})
    return object_id_to_str(created_item)

@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: str):
    item = await items_collection.find_one({"_id": ObjectId(item_id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return object_id_to_str(item)

@router.get("/", response_model=List[Item])
async def filter_items(
    email: Optional[str] = None,
    expiry_date: Optional[date] = None,
    insert_date: Optional[datetime] = None,
    quantity: Optional[int] = Query(None, ge=0)
):
    query = {}
    if email:
        query["email"] = email
    if expiry_date:
        query["expiry_date"] = {"$gte": expiry_date}
    if insert_date:
        query["insert_date"] = {"$gte": insert_date}
    if quantity is not None:
        query["quantity"] = {"$gte": quantity}
    
    items = await items_collection.find(query).to_list(length=None)
    return [object_id_to_str(item) for item in items]

@router.get("/aggregate/count-by-email")
async def aggregate_items_by_email():
    pipeline = [
        {
            "$group": {
                "_id": "$email",
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "email": "$_id",
                "count": 1,
                "_id": 0
            }
        }
    ]
    
    result = await items_collection.aggregate(pipeline).to_list(length=None)
    return result

@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: str):
    delete_result = await items_collection.delete_one({"_id": ObjectId(item_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")

@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: str, item: ItemCreate):
    update_data = item.dict(exclude_unset=True)
    if 'expiry_date' in update_data and isinstance(update_data['expiry_date'], date):
        update_data['expiry_date'] = datetime.combine(update_data['expiry_date'], datetime.min.time())

    updated_item = await items_collection.find_one_and_update(
        {"_id": ObjectId(item_id)},
        {"$set": update_data},
        return_document=True
    )
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return object_id_to_str(updated_item)