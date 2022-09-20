import datetime

import pandas as pd
import streamlit as st

from pages.booking import read_booking
from pages.room import read_room
from pages.user import read_user


st.title('会議室予約システム')

st.write('### 予約一覧')
bookings = read_booking()
df_bookings = pd.DataFrame(bookings)
if bookings:
    # 予約があれば表示する
    users = read_user()
    rooms = read_room()

    users_id = {}
    for user in users:
        users_id[user['user_id']] = user['user_name']

    rooms_id = {}
    for room in rooms:
        rooms_id[room['room_id']] = {
            'room_name': room['room_name'],
            'capacity': room['capacity'],
        }

    # ID -> 値に変更
    to_user_name = lambda x: users_id[x]  # noqa: E731
    to_room_name = lambda x: rooms_id[x]['room_name']  # noqa: E731
    to_datetime = lambda x: \
        datetime.datetime.fromisoformat(x) \
        .strftime('%Y/%m/%d %H:%M')  # noqa: E731

    df_bookings['user_id'] = df_bookings['user_id'].map(to_user_name)
    df_bookings['room_id'] = df_bookings['room_id'].map(to_room_name)
    df_bookings['start_datetime'] = \
        df_bookings['start_datetime'].map(to_datetime)
    df_bookings['end_datetime'] = \
        df_bookings['end_datetime'].map(to_datetime)

    df_bookings_ja = df_bookings.rename(columns={
        'user_id': '予約者名',
        'room_id': '会議室名',
        'num_people': '予約人数',
        'start_datetime': '開始時刻',
        'end_datetime': '終了時刻',
        'booking_id': '予約番号'
    })

    st.table(df_bookings_ja)
else:
    st.write('現在予約はありません')
