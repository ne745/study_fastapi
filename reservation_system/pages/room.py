import configparser
import json

import requests
import streamlit as st


config = configparser.ConfigParser()
config.read('./pages/config.ini')

HOST = config['WEB_SERVEER']['host']
PORT = config['WEB_SERVEER']['port']
PAGE = config['WEB_SERVEER']['room']
URL_ROOM = f'http://{HOST}:{PORT}/{PAGE}'


def read_room():
    # 会議室一覧の取得
    res = requests.get(URL_ROOM)
    rooms = res.json()
    return rooms


def generate_rooms_name():
    rooms = read_room()
    # キー: 会議室名, バリュー: 会議室 ID, 定員
    rooms_name = {}
    for room in rooms:
        rooms_name[room['room_name']] = {
            'room_id': room['room_id'],
            'capacity': room['capacity'],
        }
    return rooms_name


def create_room():
    # 登録
    st.write('## 登録')
    with st.form(key=PAGE):
        room_name: str = st.text_input('会議室名', max_chars=12)
        capacity: int = st.number_input('定員', step=1, min_value=1)
        data = {
            'room_name': room_name,
            'capacity': capacity
        }
        submit_button = st.form_submit_button(label='会議室登録')

    if submit_button:
        st.write('## レスポンス結果')
        res = requests.post(URL_ROOM, json.dumps(data))

        if res.status_code == 200:
            st.success('会議室登録完了')
        else:
            st.error('会議室登録失敗')
            st.write(res.status_code)
        st.json(res.json())


def delete_room():
    # 削除
    rooms_name = generate_rooms_name()

    st.write(rooms_name)

    if rooms_name:
        st.write('## 削除')
        with st.form(key=PAGE + '-DELETE'):
            room_name = st.selectbox('会議室名', rooms_name.keys())
            is_clicked_delete_button = st.form_submit_button(label='会議室削除')

        if is_clicked_delete_button:
            data = {'room_id': rooms_name[room_name]['room_id']}
            res = requests.delete(URL_ROOM, params=data)

            if res.status_code == 200:
                st.success('会議室削除完了')
            else:
                st.error('会議室削除失敗')
                st.write(res.status_code)
            st.json(res.json())


st.title('会議室設定画面')

create_room()
delete_room()
