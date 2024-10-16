from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


items = [
    Item(id=1, name="Item 1", description="Description 1"),
    Item(id=2, name="Item 2", description="Description 2"),
]


@app.get("/api", tags=["Default"])
async def root():
    return {
        "status": "ok",
    }


@app.get("/api/items", response_model=List[Item], tags=["Items"])
async def get_items():
    return items


@app.post("/api/items", response_model=Item, tags=["Items"])
async def create_item(item: Item):
    items.append(item)
    return item


@app.get("/api/items/{item_id}", response_model=Item, tags=["Items"])
async def get_item(item_id: int):
    item = next((item for item in items if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/api/items/{item_id}", response_model=Item, tags=["Items"])
async def update_item(item_id: int, updated_item: Item):
    index = next((index for index, item in enumerate(items) if item.id == item_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    items[index] = updated_item
    return updated_item


@app.delete("/api/items/{item_id}", tags=["Items"])
async def delete_item(item_id: int):
    global items
    items = [item for item in items if item.id != item_id]
    return {"status": "Item deleted"}
