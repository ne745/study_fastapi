from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from sql_app import crud
from sql_app import models
from sql_app.database import SessionLocal, engine
from sql_app.schemas import (
    BookingCreate, UserCreate, RoomCreate,
    Booking, User, Room
)


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
async def create_booking(
        booking: BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db, booking)


@app.post('/users', response_model=User)
async def create_user(
        user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.post('/rooms', response_model=Room)
async def create_room(
        room: RoomCreate, db: Session = Depends(get_db)):
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


##############################
# DELETE #####################
##############################
@app.delete('/bookings')
async def delete_booking(
        booking_id: int, db: Session = Depends(get_db)):
    return crud.delete_booking(db, booking_id)


@app.delete('/users')
async def delete_user(
        user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id)


@app.delete('/rooms')
async def delete_room(
        room_id: int, db: Session = Depends(get_db)):
    return crud.delete_room(db, room_id)
