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
    db_used_user_name = db.query(models.User).\
        filter(models.User.user_name == user.user_name)
    if db_used_user_name:
        raise HTTPException(status_code=404, detail='Already used')

    db_user = models.User(user_name=user.user_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_room(db: Session, room: schemas.Room):
    # 会議室登録
    db_used_room_name = db.query(models.Room).\
        filter(models.Room.room_name == room.room_name)
    if db_used_room_name:
        raise HTTPException(status_code=404, detail='Already used')

    db_room = models.Room(room_name=room.room_name, capacity=room.capacity)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


##############################
# READ #######################
##############################
def get_bookings(db: Session):
    # 予約一覧取得
    return db.query(models.Booking).all()


def get_users(db: Session):
    # ユーザ一覧取得
    return db.query(models.User).all()


def get_rooms(db: Session):
    # 会議室一覧取得
    return db.query(models.Room).all()


##############################
# UPDATE #####################
##############################
def update_booking(db: Session, booking: schemas.Booking):
    # 予約更新
    # 既存の予約と重複があるか検証
    db_booked = db.query(models.Booking).\
        filter(models.Booking.booking_id != booking.booking_id).\
        filter(models.Booking.room_id == booking.room_id).\
        filter(models.Booking.end_datetime > booking.start_datetime).\
        filter(models.Booking.start_datetime < booking.end_datetime).\
        all()

    if not db_booked:
        target_booking = db.query(models.Booking)\
            .filter(models.Booking.booking_id == booking.booking_id)
        target_booking.update({
            models.Booking.user_id: booking.user_id,
            models.Booking.room_id: booking.room_id,
            models.Booking.num_people: booking.num_people,
            models.Booking.start_datetime: booking.start_datetime,
            models.Booking.end_datetime: booking.end_datetime
        })
        db.commit()
        return {'message': 'success'}
    else:
        raise HTTPException(status_code=404, detail='Already booked')


def update_user(db: Session, user: schemas.User):
    # ユーザ登録
    target_user = db.query(models.User)\
        .filter(models.User.user_id == user.user_id)
    target_user.update({
        models.User.user_name: user.user_name
    })
    db.commit()
    return {'message': 'success'}


def update_room(db: Session, room: schemas.Room):
    # 会議室更新
    target_room = db.query(models.Room)\
        .filter(models.Room.room_id == room.room_id)
    target_room.update({
        models.Room.room_name: room.room_name,
        models.Room.capacity: room.capacity
    })
    db.commit()
    return {'message': 'success'}


##############################
# DELETE #####################
##############################
def delete_booking(db: Session, booking_id: int):
    # 予約削除
    target_booking = db.query(models.Booking)\
        .filter(models.Booking.booking_id == booking_id)
    target_booking.delete()
    db.commit()
    return {'message': 'success'}


def delete_user(db: Session, user_id: int):
    # ユーザ削除
    target_user = db.query(models.User).filter(models.User.user_id == user_id)
    target_user.delete()
    db.commit()

    # 削除するユーザが登録している予約も削除
    target_booking = db.query(models.Booking)\
        .filter(models.Booking.user_id == user_id)
    target_booking.delete()

    return {'message': 'success'}


def delete_room(db: Session, room_id: int):
    # 会議室削除
    target_room = db.query(models.Room).filter(models.Room.room_id == room_id)
    target_room.delete()

    # 削除するユーザが登録している予約も削除
    target_booking = db.query(models.Booking)\
        .filter(models.Booking.room_id == room_id)
    target_booking.delete()

    db.commit()
    return {'message': 'success'}
