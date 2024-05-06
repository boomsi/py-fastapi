from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

@app.get('/')
async def root():
    return dict(message='Hello world')

@app.post('/registry')
async def registry(user: User):
    print(user)
    return user