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
async def read_bookings(db: Session = Depends(get_db)):
    return crud.get_bookings(db)


@app.get('/users', response_model=List[User])
async def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.get('/rooms', response_model=List[Room])
async def read_rooms(db: Session = Depends(get_db)):
    return crud.get_rooms(db)


##############################
# UPDATE #####################
##############################
@app.put('/bookings')
async def update_booking(
        booking: Booking, db: Session = Depends(get_db)):
    return crud.update_booking(db, booking)


@app.put('/users')
async def update_user(
        user: User, db: Session = Depends(get_db)):
    return crud.update_user(db, user)


@app.put('/rooms')
async def update_room(
        room: Room, db: Session = Depends(get_db)):
    return crud.update_room(db, room)


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
