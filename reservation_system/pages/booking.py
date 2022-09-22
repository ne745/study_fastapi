import configparser
import datetime
import json

import pandas as pd
import requests
import streamlit as st

from pages.room import generate_rooms_name, read_room
from pages.user import generate_user_name, read_user


config = configparser.ConfigParser()
config.read('./pages/config.ini')

HOST = config['WEB_SERVEER']['host']
PORT = config['WEB_SERVEER']['port']
PAGE = config['WEB_SERVEER']['booking']
URL_BOOKING = f'http://{HOST}:{PORT}/{PAGE}'


def read_booking():
    # 予約一覧の取得
    res = requests.get(URL_BOOKING)
    bookings = res.json()
    return bookings


def generate_booking_table():
    bookings = read_booking()
    df_bookings = pd.DataFrame(bookings)
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
    return df_bookings_ja


def create_booking():
    users_name = generate_user_name()
    rooms_name = generate_rooms_name()

    if not users_name:
        st.error('ユーザを登録してください')
    if not rooms_name:
        st.error('会議室を登録してください')

    if not (users_name and rooms_name):
        return

    st.write('### 会議室一覧')
    rooms = read_room()
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ['会議室名', '定員', '会議室 ID']
    st.table(df_rooms)

    st.write('## 予約')
    with st.form(key=PAGE):
        user_name = st.selectbox('予約者名', users_name.keys())
        room_name = st.selectbox('会議室名', rooms_name.keys())
        num_people: int = st.number_input('人数', step=1, min_value=1)
        date = st.date_input('日付を入力', min_value=datetime.date.today())
        start_time = st.time_input(
            '開始時刻', value=datetime.time(hour=9, minute=0))
        end_time = st.time_input(
            '修了時刻', value=datetime.time(hour=20, minute=0))
        start_datetime = datetime.datetime(
            year=date.year, month=date.month, day=date.day,
            hour=start_time.hour, minute=start_time.minute
        )
        end_datetime = datetime.datetime(
            year=date.year, month=date.month, day=date.day,
            hour=end_time.hour, minute=end_time.minute
        )
        submit_button = st.form_submit_button(label='送信')

    if submit_button:
        user_id = users_name[user_name]
        room_id = rooms_name[room_name]['room_id']
        capacity = rooms_name[room_name]['capacity']
        data = {
            'user_id': user_id,
            'room_id': room_id,
            'num_people': num_people,
            'start_datetime': start_datetime.isoformat(),
            'end_datetime': end_datetime.isoformat()
        }

        if num_people > capacity:
            # 予約人数の検証
            st.error(f'{room_name} の定員は {capacity} 名です．')
        elif start_time >= end_time:
            # 開始時刻修了時刻の検証
            st.error('開始時刻が修了時刻より遅く設定されています．')
        elif start_time < datetime.time(hour=9, minute=0):
            st.error('利用可能時間は 9:00 ~ 20:00 になります．')
        elif end_time > datetime.time(hour=20, minute=0):
            st.error('利用可能時間は 9:00 ~ 20:00 になります．')
        else:
            st.write('## レスポンス結果')
            res = requests.post(URL_BOOKING, json.dumps(data))
            if res.status_code == 200:
                st.success('予約完了')
            elif res.status_code == 404 \
                    and res.json()['detail'] == 'Already booked':
                st.error('指定の時間は既に予約されています．')
            else:
                st.error('予約失敗')
                st.write(res.status_code)


def update_booking():
    bookings = read_booking()
    if not bookings:
        return

    st.write('## 更新')
    df_bookings_ja = generate_booking_table()
    st.table(df_bookings_ja)

    booking_ids = df_bookings_ja['予約番号'].to_list()
    booking_id = st.selectbox('予約番号', booking_ids)

    old_booking = df_bookings_ja[df_bookings_ja['予約番号'] == booking_id]
    old_booking_idx = df_bookings_ja['予約番号'].to_list().index(booking_id)
    with st.form(key=PAGE + '-update'):
        old_start_datetime = datetime.datetime.strptime(
            old_booking['開始時刻'].iloc[0], '%Y/%m/%d %H:%M')
        old_end_datetime = datetime.datetime.strptime(
            old_booking['終了時刻'].iloc[0], '%Y/%m/%d %H:%M')
        old_date = datetime.date(
            year=old_start_datetime.year,
            month=old_start_datetime.month,
            day=old_start_datetime.day
        )
        old_start_time = datetime.time(
            hour=old_start_datetime.hour, minute=old_start_datetime.minute)
        old_end_time = datetime.time(
            hour=old_end_datetime.hour, minute=old_end_datetime.minute)

        new_user_name = st.selectbox(
            '予約者名', df_bookings_ja['予約者名'].tolist(),
            index=old_booking_idx)
        new_room_name = st.selectbox(
            '会議室名', df_bookings_ja['会議室名'].tolist(),
            index=old_booking_idx)
        new_num_people = st.number_input(
            '人数', step=1, min_value=1, value=old_booking['予約人数'].iloc[0])
        new_date = st.date_input(
            '日付を入力', min_value=datetime.date.today(), value=old_date)
        new_start_time = st.time_input(
            '開始時刻', value=old_start_time)
        new_end_time = st.time_input(
            '終了時刻', value=old_end_time)
        new_start_datetime = datetime.datetime(
            year=new_date.year, month=new_date.month, day=new_date.day,
            hour=new_start_time.hour, minute=new_start_time.minute
        )
        new_end_datetime = datetime.datetime(
            year=new_date.year, month=new_date.month, day=new_date.day,
            hour=new_end_time.hour, minute=new_end_time.minute
        )

        is_clicked_update_button = st.form_submit_button(label='予約更新')

    if is_clicked_update_button:
        users_name = generate_user_name()
        rooms_name = generate_rooms_name()
        new_user_id = users_name[new_user_name]
        new_room_id = rooms_name[new_room_name]['room_id']
        new_capacity = rooms_name[new_room_name]['capacity']
        data = {
            'user_id': new_user_id,
            'room_id': new_room_id,
            'num_people': new_num_people,
            'start_datetime': new_start_datetime.isoformat(),
            'end_datetime': new_end_datetime.isoformat(),
            'booking_id': booking_id
        }

        if new_num_people > new_capacity:
            # 予約人数の検証
            st.error(f'{new_room_name} の定員は {new_capacity} 名です．')
        elif new_start_time >= new_end_time:
            # 開始時刻修了時刻の検証
            st.error('開始時刻が修了時刻より遅く設定されています．')
        elif new_start_time < datetime.time(hour=9, minute=0):
            st.error('利用可能時間は 9:00 ~ 20:00 になります．')
        elif new_end_time > datetime.time(hour=20, minute=0):
            st.error('利用可能時間は 9:00 ~ 20:00 になります．')
        else:
            st.write('## レスポンス結果')
            res = requests.put(URL_BOOKING, json.dumps(data))
            if res.status_code == 200:
                st.success('予約更新完了')
            elif res.status_code == 404 \
                    and res.json()['detail'] == 'Already booked':
                st.error('指定の時間は既に予約されています．')
            else:
                st.error('予約更新失敗')
                st.write(res.status_code)


def delete_booking():
    bookings = read_booking()
    df_bookings = pd.DataFrame(bookings)

    if bookings:
        st.write('## 削除')
        with st.form(key=PAGE + '-delete'):
            booking_ids = df_bookings['booking_id'].to_list()
            booking_id = st.selectbox('予約番号', booking_ids)
            is_clicked_delete_button = st.form_submit_button(label='予約削除')

        if is_clicked_delete_button:
            data = {'booking_id': booking_id}
            res = requests.delete(URL_BOOKING, params=data)

            if res.status_code == 200:
                st.success('予約削除完了')
            else:
                st.error('予約削除失敗')
                st.write(res.status_code)
            st.json(res.json())


def main():
    st.title('予約設定画面')
    create_booking()
    update_booking()
    delete_booking()


if __name__ == '__main__':
    main()
