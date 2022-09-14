from sqlalchemy.orm import Session
import models


# READ
def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    # 予約一覧取得
    return db.query(models.Booking).offset(skip).limit(limit).all()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    # ユーザ一覧取得
    return db.query(models.User).offset(skip).limit(limit).all()


def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    # 会議室一覧取得
    return db.query(models.Room).offset(skip).limit(limit).all()
