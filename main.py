from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from database import SessionLocal, engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import select
from typing import Dict, List
import models

description = """
This API app helps you do awesome stuff. 🚀

"""

app = FastAPI(
        title="Atlas API app",
        description=description,
        version="0.1.0",
        summary="This is a summary of this app"
        )

class Item(BaseModel):
    id:int
    name:str
    description:str
    price:int
    on_offer:bool

    class Config:
        from_attributes=True # help pydantic serialize SQLAlchemy objects

db = SessionLocal()

@app.get("/status", response_model=Dict[str, str])
def get_status():
    breakpoint()
    try:
        with engine.connect() as connection:
            connection.execute(select(1))
            return {"status": "OK"}

    except OperationalError:
        raise HTTPException(status_code=500, detail="Failed to connect to the database.")

@app.get('/items', response_model=List[Item], status_code=200)
def get_all_items():
    items = db.query(models.Item).all()
    
    return items

@app.get('/item/{item_id}', response_model=Item, status_code=status.HTTP_200_OK)
def get_item(item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    return item
    
@app.post('/items', response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    new_item=models.Item(
            name=item.name,
            price=item.price,
            description=item.description,
            on_offer=item.on_offer
            )

    db_item = db.query(models.Item).filter(models.Item.name == new_item.name).first()
    if db_item is not None:
        raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "name must be unique"
                )

    db.add(new_item)
    db.commit()

    return new_item # pydantic will automatically serialize to JSON


@app.put('/item/{item_id}', response_model=Item, status_code=status.HTTP_200_OK)
def update_item(item_id: int, item: Item):
    item_to_update = db.query(models.Item).filter(models.Item.id == item_id).first()
    item_to_update.name = item.name
    item_to_update.description = item.description
    item_to_update.price = item.price
    item_to_update.on_offer = item.on_offer

    return item_to_update

@app.delete('/item/{item_id}', response_model=Item, status_code=status.HTTP_200_OK)
def delete_item(item_id: int):
    item_to_delete = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item_to_delete is None:
        raise HTTPException( status.HTTP_404_NOT_FOUND, "resource not found")

    db.delete(item_to_delete)
    db.commit()

    return item_to_delete
