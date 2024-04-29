from fastapi import Depends, FastAPI, HTTPException, Response, Request
from sqlalchemy.orm import Session

from . import curd, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 中间件方式
# @app.middleware('http')
# async def db_session_middleware(request, call_next):
#     response = Response("Internal server error", status_code=500)
#     try:
#         request.state.db = SessionLocal()
#         response = await call_next(request)
#     finally:
#         request.state.db.close()
#     return response

# def get_db(request: Request):
#     return request.state.db

@app.post('/users', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = curd.get_user_by_email(db, email = user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return curd.create_user(db=db, user=user)
