from typing import Annotated, Dict
from enum import Enum

from fastapi import FastAPI, Query, Path, Body, Cookie, Header, Depends
from pydantic import BaseModel, Field

app = FastAPI()

class ModelName(str, Enum):
    alexnet = 'alexnet',
    resnet = 'resnet',
    lenet = 'lenet'

    model_config = dict(
        json_schema_extra=dict(
            examples=[
                dict(
                    alexnet='Deep Learning FTW!',
                    resnet='Have some residuals',
                    lenet='LeCNN all'
                )
            ]
        )
    )

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float = Field(gt=10)
    tax: float | None = None

@app.get('/')
def read_root():
    return dict(a=1)

@app.get('/item/{item_id}')
def read_item(item_id: Annotated[int, Path(gt=1)], q: str | None = None):
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


# @app.get('/items')
# async def get_items(page: int = 0, limit: int = 10):
#     return dict(page=page, limit=limit)


@app.get('/items')
def get_items(page: Annotated[int, Query(gt=100)] = 101, limit: int = Query(max=50, deprecated=True)):
    return dict(page=page, limit=limit)

@app.post('/abc')
def get_abc(item: Item, importance: Annotated[int, Body(gt=0)]):
    return dict(importance=importance)


@app.get('/cookie')
def get_cookie(ad: Annotated[str, Cookie()]):
    return dict(ad=ad)

@app.get('/header', response_model=Item, response_model_include=['price'], response_model_exclude_unset=True)
def get_header(token: Annotated[str, Header()]) -> Item:
    return Item(name=token, price=10.5)


# def get_depend_common(q: Dict[str, int]):
#     new_q = dict()
#     for k, v in q.items():
#         new_q[k] = v + 1
#     return new_q

class CommonDepends:
    def __init__(self, common: str, q: int):
        self.common = common
        self.q = q + 10086

@app.get('/depends')
def get_depend(commons: Annotated[CommonDepends, Depends(CommonDepends)]):
    return commons
