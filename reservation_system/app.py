import json
import random

import requests
import streamlit as st


URL = 'http://localhost:8000'


page = st.sidebar.selectbox('Choose your page', ['user', 'room'])

if page == 'user':
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
