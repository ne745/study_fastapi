from fastapi import HTTPException
from sqlalchemy.orm import Session

from sql_app import models
from sql_app import schemas


##############################
# CREATE #####################
##############################
def create_booking(db: Session, booking: schemas.Booking):
    # 予約登録
    # 既存の予約と重複があるか検証
    db_booked = db.query(models.Booking).\
        filter(models.Booking.room_id == booking.room_id).\
        filter(models.Booking.end_datetime > booking.start_datetime).\
        filter(models.Booking.start_datetime < booking.end_datetime).\
        all()

    if not db_booked:
        # 重複なし
        db_booking = models.Booking(
            user_id=booking.user_id,
            room_id=booking.room_id,
            num_people=booking.num_people,
            start_datetime=booking.start_datetime,
            end_datetime=booking.end_datetime
        )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        return db_booking
    else:
        raise HTTPException(status_code=404, detail='Already booked')


def create_user(db: Session, user: schemas.User):
    # ユーザ登録
    db_user = models.User(user_name=user.user_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_room(db: Session, room: schemas.Room):
    # 会議室登録
    db_room = models.Room(room_name=room.room_name, capacity=room.capacity)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


##############################
# READ #######################
##############################
def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    # 予約一覧取得
    return db.query(models.Booking).offset(skip).limit(limit).all()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    # ユーザ一覧取得
    return db.query(models.User).offset(skip).limit(limit).all()


def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    # 会議室一覧取得
    return db.query(models.Room).offset(skip).limit(limit).all()


##############################
# DELETE #####################
##############################
def delete_user(db: Session, user_id: int):
    # ユーザ削除
    target_user = db.query(models.User).filter(models.User.user_id == user_id)
    target_user.delete()
    db.commit()
    return {'message': 'success'}
