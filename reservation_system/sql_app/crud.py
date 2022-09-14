from sqlalchemy.orm import Session
import models
import schemas


##############################
# CREATE #####################
##############################
def create_booking(db: Session, booking: schemas.Booking):
    # 予約登録
    db_booking = models.Booking(
        user_id=booking.user_id,
        room_id=booking.room_id,
        num_people=booking.num_people,
        start_datetime=booking.start_time,
        end_datetime=booking.end_time
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


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
