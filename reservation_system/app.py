import datetime
import json

import pandas as pd
import requests
import streamlit as st


URL = 'http://localhost:8000'
URL_BOOKING = f'{URL}/bookings'
URL_USERS = f'{URL}/users'
URL_ROOMS = f'{URL}/rooms'


page_name = {
    '予約': 'booking',
    'ユーザ': 'user',
    '会議室': 'room',
}
page_ja = st.sidebar.selectbox(
    '設定画面を選んでください', page_name.keys(), index=0)

page = page_name[page_ja]

# 予約一覧の取得
res = requests.get(URL_BOOKING)
bookings = res.json()
df_bookings = pd.DataFrame(bookings)

# ユーザ一覧の取得
res = requests.get(URL_USERS)
users = res.json()
# キー: ユーザ名, バリュー: ユーザ ID
users_name = {}
for user in users:
    users_name[user['user_name']] = user['user_id']

# 会議室一覧の取得
res = requests.get(URL_ROOMS)
rooms = res.json()
# キー: 会議室名, バリュー: 会議室 ID, 定員
rooms_name = {}
for room in rooms:
    rooms_name[room['room_name']] = {
        'room_id': room['room_id'],
        'capacity': room['capacity'],
    }


if page == 'booking':
    st.title('会議室設定画面')

    if not users:
        st.error('ユーザを登録してください')
    if not rooms:
        st.error('会議室を登録してください')

    st.write('### 会議室一覧')
    if rooms:
        df_rooms = pd.DataFrame(rooms)
        df_rooms.columns = ['会議室名', '定員', '会議室 ID']
        st.table(df_rooms)
    else:
        st.write('予約可能な会議室はありません')

    st.write('### 予約一覧')
    if bookings:
        # 予約があれば表示する
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

    st.write('## 予約')
    with st.form(key=page):
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

    # 削除
    if bookings:
        st.write('## 削除')
        with st.form(key=page + '-delete'):
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

elif page == 'user':
    st.title('ユーザ設定画面')

    # 登録
    st.write('## 登録')
    with st.form(key=page):
        user_name: str = st.text_input('ユーザ名', max_chars=12)
        data = {
            'user_name': user_name
        }
        submit_button = st.form_submit_button(label='ユーザ登録')

    if submit_button:
        st.write('## レスポンス結果')
        res = requests.post(URL_USERS, json.dumps(data))

        if res.status_code == 200:
            st.success('ユーザ登録完了')
        else:
            st.error('ユーザ登録失敗')
            st.write(res.status_code)
        st.json(res.json())

    # 削除
    if users:
        st.write('## 削除')
        with st.form(key=page + '-delete'):
            user_name = st.selectbox('ユーザ名', users_name.keys())
            is_clicked_delete_button = st.form_submit_button(label='ユーザ削除')

        if is_clicked_delete_button:
            data = {'user_id': users_name[user_name]}
            res = requests.delete(URL_USERS, params=data)

            if res.status_code == 200:
                st.success('ユーザ削除完了')
            else:
                st.error('ユーザ削除失敗')
                st.write(res.status_code)
            st.json(res.json())

elif page == 'room':
    st.title('会議室設定画面')

    # 登録
    st.write('## 登録')
    with st.form(key=page):
        room_name: str = st.text_input('会議室名', max_chars=12)
        capacity: int = st.number_input('定員', step=1, min_value=1)
        data = {
            'room_name': room_name,
            'capacity': capacity
        }
        submit_button = st.form_submit_button(label='会議室登録')

    if submit_button:
        st.write('## レスポンス結果')
        res = requests.post(URL_ROOMS, json.dumps(data))

        if res.status_code == 200:
            st.success('会議室登録完了')
        else:
            st.error('会議室登録失敗')
            st.write(res.status_code)
        st.json(res.json())

    # 削除
    if rooms:
        st.write('## 削除')
        with st.form(key=page + '-delete'):
            room_name = st.selectbox('会議室名', rooms_name.keys())
            is_clicked_delete_button = st.form_submit_button(label='会議室削除')

        if is_clicked_delete_button:
            data = {'room_id': rooms_name[room_name]['room_id']}
            res = requests.delete(URL_ROOMS, params=data)

            if res.status_code == 200:
                st.success('会議室削除完了')
            else:
                st.error('会議室削除失敗')
                st.write(res.status_code)
            st.json(res.json())
