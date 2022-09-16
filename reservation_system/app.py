import datetime
import json

import pandas as pd
import requests
import streamlit as st


URL = 'http://localhost:8000'


page = st.sidebar.selectbox(
    'Choose your page', ['booking', 'user', 'room'], index=0)

if page == 'booking':
    st.title('会議室予約画面')

    # ユーザ一覧の取得
    url_users = URL + '/users'
    res = requests.get(url_users)
    users = res.json()

    # キー: ユーザ名, バリュー: ユーザ ID
    users_name = {}
    for user in users:
        users_name[user['user_name']] = user['user_id']

    # 会議室一覧の取得
    url_rooms = URL + '/rooms'
    res = requests.get(url_rooms)
    rooms = res.json()

    # キー: 会議室名, バリュー: 会議室 ID
    rooms_name = {}
    for room in rooms:
        rooms_name[room['room_name']] = {
            'room_id': room['room_id'],
            'capacity': room['capacity'],
        }

    st.write('### 会議室一覧')
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ['会議室名', '定員', '会議室 ID']
    st.table(df_rooms)

    # 会議室一覧の取得
    url_bookings = URL + '/bookings'
    res = requests.get(url_bookings)
    bookings = res.json()
    df_bookings = pd.DataFrame(bookings)

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
    to_user_name = lambda x: users_id[x]
    to_room_name = lambda x: rooms_id[x]['room_name']
    to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime('%Y/%m/%d %H:%M')

    df_bookings['user_id'] = df_bookings['user_id'].map(to_user_name)
    df_bookings['room_id'] = df_bookings['room_id'].map(to_room_name)
    df_bookings['start_datetime'] = df_bookings['start_datetime'].map(to_datetime)
    df_bookings['end_datetime'] = df_bookings['end_datetime'].map(to_datetime)

    df_bookings = df_bookings.rename(columns={
        'user_id': '予約者名',
        'room_id': '会議室名',
        'num_people': '予約人数',
        'start_datetime': '開始時刻',
        'end_datetime': '終了時刻',
        'booking_id': '予約番号'
    })

    st.write('### 予約一覧')
    st.table(df_bookings)

    with st.form(key=page):
        user_name = st.selectbox('予約者名', users_name.keys())
        room_name = st.selectbox('会議室名', rooms_name.keys())
        num_people: int = st.number_input('人数', step=1, min_value=1)
        date = st.date_input('日付を入力', min_value=datetime.date.today())
        start_time = st.time_input(
            '開始時刻', value=datetime.time(hour=9, minute=0), )
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

        # 予約人数の検証
        if num_people <= capacity:
            st.write('## レスポンス結果')
            res = requests.post(URL + '/bookings', json.dumps(data))
            if res.status_code == 200:
                st.success('予約完了')
            else:
                st.success('予約失敗')
                st.write(res.status_code)
            st.json(res.json())
        else:
            st.error(f'{room_name} の定員は {capacity} 名です．')


elif page == 'user':
    st.title('ユーザ登録画面')
    with st.form(key=page):
        user_name: str = st.text_input('ユーザ名', max_chars=12)
        data = {
            'user_name': user_name
        }
        submit_button = st.form_submit_button(label='ユーザ登録')

    if submit_button:
        st.write('## レスポンス結果')
        res = requests.post(URL + '/users', json.dumps(data))

        if res.status_code == 200:
            st.success('ユーザ登録完了')
        else:
            st.success('ユーザ登録失敗')
            st.write(res.status_code)
        st.json(res.json())

elif page == 'room':
    st.title('会議室登録画面')
    with st.form(key=page):
        room_name: str = st.text_input('会議室名', max_chars=12)
        capacity: int = st.number_input('定員', step=1)
        data = {
            'room_name': room_name,
            'capacity': capacity
        }
        submit_button = st.form_submit_button(label='会議室登録')

    if submit_button:
        st.write('## レスポンス結果')
        res = requests.post(URL + '/rooms', json.dumps(data))

        if res.status_code == 200:
            st.success('ユーザ登録完了')
        else:
            st.success('ユーザ登録失敗')
            st.write(res.status_code)
        st.json(res.json())
