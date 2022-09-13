import datetime
import json
import random

import requests
import streamlit as st


URL = 'http://localhost:8000'


page = st.sidebar.selectbox(
    'Choose your page', ['booking', 'user', 'room'], index=1)

if page == 'booking':
    st.title('API テスト画面 (予約)')
    with st.form(key=page):
        booking_id: int = random.randint(0, 10)
        user_id: int = random.randint(0, 10)
        room_id: int = random.randint(0, 10)
        num_people: int = st.number_input('人数', step=1)
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
        data = {
            'booking_id': booking_id,
            'user_id': user_id,
            'room_id': room_id,
            'num_people': num_people,
            'start_datetime': start_datetime.isoformat(),
            'end_datetime': end_datetime.isoformat()
        }
        submit_button = st.form_submit_button(label='送信')

    if submit_button:
        st.write('## 送信データ')
        st.json(data)

        st.write('## レスポンス結果')
        res = requests.post(URL + '/bookings', json.dumps(data))
        st.write(res.status_code)
        st.json(res.json())


elif page == 'user':
    st.title('API テスト画面 (ユーザ)')
    with st.form(key=page):
        user_id: int = random.randint(0, 10)
        user_name: str = st.text_input('ユーザ名', max_chars=12)
        data = {
            'user_id': user_id,
            'user_name': user_name
        }
        submit_button = st.form_submit_button(label='送信')

    if submit_button:
        st.write('## 送信データ')
        st.json(data)

        st.write('## レスポンス結果')
        res = requests.post(URL + '/users', json.dumps(data))
        st.write(res.status_code)
        st.json(res.json())

elif page == 'room':
    st.title('API テスト画面 (会議室)')
    with st.form(key=page):
        room_id: int = random.randint(0, 10)
        room_name: str = st.text_input('会議室名', max_chars=12)
        capacity: int = st.number_input('定員', step=1)
        data = {
            'room_id': room_id,
            'room_name': room_name,
            'capacity': capacity
        }
        submit_button = st.form_submit_button(label='送信')

    if submit_button:
        st.write('## 送信データ')
        st.json(data)

        st.write('## レスポンス結果')
        res = requests.post(URL + '/rooms', json.dumps(data))
        st.write(res.status_code)
        st.json(res.json())
