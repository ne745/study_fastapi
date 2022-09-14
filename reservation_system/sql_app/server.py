from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import models
from database import SessionLocal, engine
from schemas import Booking, User, Room


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get('/')
# async def index():
#     return {'message': 'Success'}


##############################
# CREATE #####################
##############################
@app.post('/bookings', response_model=Booking)
async def create_booking(booking: Booking, db: Session = Depends(get_db)):
    return crud.create_booking(db, booking)


@app.post('/users', response_model=User)
async def create_user(user: User, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.post('/rooms', response_model=Room)
async def create_room(room: Room, db: Session = Depends(get_db)):
    return crud.create_room(db, room)


##############################
# READ #######################
##############################
@app.get('/bookings', response_model=List[Booking])
async def read_bookings(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bookings = crud.get_bookings(db, skip, limit)
    return bookings


@app.get('/users', response_model=List[User])
async def read_users(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, limit)
    return users


@app.get('/rooms', response_model=List[Room])
async def read_rooms(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rooms = crud.get_rooms(db, skip, limit)
    return rooms
