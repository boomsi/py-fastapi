from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get('/')
def read_root():
    return dict(a=1)

@app.get('/item/{item_id}')
def read_item(item_id:int, q: Union[str, None] = None):
    return dict(
        item_id=item_id,
        q=q
    )

@app.put('/item/{item_id}')
def update_item(item_id: int, item: Item):
    return dict(
        item_id=item_id,
        item_name=item.name
    )
