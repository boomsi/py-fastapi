from typing import Union
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ModelName(str, Enum):
    alexnet = 'alexnet',
    resnet = 'resnet',
    lenet = 'lenet'

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

@app.get('/models/{model_name}')
def get_module(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return dict(model_name=model_name, message='Deep Learning FTW!')
    elif model_name is ModelName.lenet:
        return dict(model_name=model_name, message='LeCNN all the images')
    elif model_name is ModelName.resnet:
        return dict(model_name=model_name, message='Have some residuals')


@app.get('/items')
async def get_items(page: int = 0, limit: int = 10):
    return dict(page=page, limit=limit)

