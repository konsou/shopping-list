from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Item(BaseModel):
    name: str
    quantity: int


shopping_list: List[Item] = []


@app.post("/items/", response_model=Item)
def add_item(item: Item) -> Item:
    shopping_list.append(item)
    return item


@app.get("/items/", response_model=List[Item])
def list_items() -> List[Item]:
    return shopping_list


@app.delete("/items/{item_name}", response_model=Item)
def remove_item(item_name: str) -> Item:
    item = next((i for i in shopping_list if i.name == item_name), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    shopping_list.remove(item)
    return item


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
