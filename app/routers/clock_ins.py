from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from ..models import ClockInRecord, ClockInRecordCreate
from app.database import get_collection, object_id_to_str

router = APIRouter()
clock_ins_collection = get_collection("clock_ins")

@router.post("/", response_model=ClockInRecord, status_code=201)
async def create_clock_in(clock_in: ClockInRecordCreate):
    clock_in_dict = clock_in.dict()
    clock_in_dict["insert_datetime"] = datetime.utcnow()
    new_clock_in = await clock_ins_collection.insert_one(clock_in_dict)
    created_clock_in = await clock_ins_collection.find_one({"_id": new_clock_in.inserted_id})
    return object_id_to_str(created_clock_in)

@router.get("/{clock_in_id}", response_model=ClockInRecord)
async def read_clock_in(clock_in_id: str):
    clock_in = await clock_ins_collection.find_one({"_id": ObjectId(clock_in_id)})
    if clock_in is None:
        raise HTTPException(status_code=404, detail="Clock-in record not found")
    return object_id_to_str(clock_in)

@router.get("/", response_model=List[ClockInRecord])
async def filter_clock_ins(
    email: Optional[str] = None,
    location: Optional[str] = None,
    insert_datetime: Optional[datetime] = None
):
    query = {}
    if email:
        query["email"] = email
    if location:
        query["location"] = location
    if insert_datetime:
        query["insert_datetime"] = {"$gte": insert_datetime}
    
    clock_ins = await clock_ins_collection.find(query).to_list(length=None)
    return [object_id_to_str(clock_in) for clock_in in clock_ins]

@router.delete("/{clock_in_id}", status_code=204)
async def delete_clock_in(clock_in_id: str):
    delete_result = await clock_ins_collection.delete_one({"_id": ObjectId(clock_in_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Clock-in record not found")

@router.put("/{clock_in_id}", response_model=ClockInRecord)
async def update_clock_in(clock_in_id: str, clock_in: ClockInRecordCreate):
    update_data = clock_in.dict(exclude_unset=True)
    updated_clock_in = await clock_ins_collection.find_one_and_update(
        {"_id": ObjectId(clock_in_id)},
        {"$set": update_data},
        return_document=True
    )
    if updated_clock_in is None:
        raise HTTPException(status_code=404, detail="Clock-in record not found")
    return object_id_to_str(updated_clock_in)