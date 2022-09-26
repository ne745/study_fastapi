import configparser
import json

import pandas as pd

import requests
import streamlit as st


config = configparser.ConfigParser()
config.read('./pages/config.ini')

HOST = config['WEB_SERVEER']['host']
PORT = config['WEB_SERVEER']['port']
PAGE = config['WEB_SERVEER']['room']
URL_ROOM = f'http://{HOST}:{PORT}/{PAGE}'


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
        elif res.status_code == 404 \
                and res.json()['detail'] == 'Already used':
            st.error(f'会議室名 {room_name} は既に使用されています．')
        else:
            st.error('会議室登録失敗')
            st.write(res.status_code)
        st.json(res.json())


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


def generate_room_table():
    rooms = read_room()
    if not rooms:
        return

    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ['会議室名', '定員', '会議室 ID']
    return df_rooms


def update_room():
    rooms_name = generate_rooms_name()

    if not rooms_name:
        return

    st.write('## 更新')
    target_room_name = st.selectbox('更新会議室名', rooms_name.keys())
    with st.form(key=PAGE + '-update'):
        new_room_name = st.text_input(
            '会議室名', value=target_room_name, max_chars=12)
        new_capacity = st.number_input(
            '定員', value=rooms_name[target_room_name]['capacity'],
            step=1, min_value=1)
        is_clicked_update_button = st.form_submit_button(label='会議室更新')

    if is_clicked_update_button:
        data = {
            'room_id': rooms_name[target_room_name]['room_id'],
            'room_name': new_room_name,
            'capacity': new_capacity
        }
        res = requests.put(URL_ROOM, data=json.dumps(data))

        if res.status_code == 200:
            st.success('会議室更新完了')
        else:
            st.error('会議室更新失敗')
            st.write(res.status_code)
        st.json(res.json())


def delete_room():
    # 削除
    rooms_name = generate_rooms_name()

    if not rooms_name:
        return

    st.write('## 削除')
    room_name = st.selectbox('削除会議室名', rooms_name.keys())
    with st.form(key=PAGE + '-DELETE'):
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


def main():
    st.title('会議室設定画面')

    df_rooms = generate_room_table()
    if df_rooms is not None:
        st.write('### 会議室一覧')
        st.table(df_rooms)
    create_room()
    update_room()
    delete_room()


if __name__ == '__main__':
    main()
