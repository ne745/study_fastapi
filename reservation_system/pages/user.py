import configparser
import json

import requests
import streamlit as st


config = configparser.ConfigParser()
config.read('./pages/config.ini')

HOST = config['WEB_SERVEER']['host']
PORT = config['WEB_SERVEER']['port']
PAGE = config['WEB_SERVEER']['user']
URL_USER = f'http://{HOST}:{PORT}/{PAGE}'


def create_user():
    # 登録
    st.write('## 登録')
    with st.form(key=PAGE):
        user_name: str = st.text_input('ユーザ名', max_chars=12)
        data = {
            'user_name': user_name
        }
        submit_button = st.form_submit_button(label='ユーザ登録')

    if submit_button:
        st.write('## レスポンス結果')
        res = requests.post(URL_USER, json.dumps(data))

        if res.status_code == 200:
            st.success('ユーザ登録完了')
        elif res.status_code == 404 \
                and res.json()['detail'] == 'Already used':
            st.error(f'ユーザ名 {user_name} は既に使用されています．')
        else:
            st.error('ユーザ登録失敗')
            st.write(res.status_code)
        st.json(res.json())


def read_user():
    # ユーザ一覧の取得
    res = requests.get(URL_USER)
    users = res.json()
    return users


def generate_user_name():
    users = read_user()
    # キー: ユーザ名, バリュー: ユーザ ID
    users_name = {}
    for user in users:
        users_name[user['user_name']] = user['user_id']
    return users_name


def update_user():
    users_name = generate_user_name()

    if not users_name:
        return

    st.write('## 更新')
    target_user_name = st.selectbox('ユーザ名', users_name.keys())
    with st.form(key=PAGE + '-update'):
        new_user_name = st.text_input(
            'ユーザ名', max_chars=12)
        is_clicked_update_button = st.form_submit_button(label='ユーザ更新')

    if is_clicked_update_button:
        data = {
            'user_id': users_name[target_user_name],
            'user_name': new_user_name
        }
        res = requests.put(URL_USER, data=json.dumps(data))

        if res.status_code == 200:
            st.success('ユーザ更新完了')
        else:
            st.error('ユーザ更新失敗')
            st.write(res.status_code)
        st.json(res.json())


def delete_user():
    # 削除
    users_name = generate_user_name()

    if users_name:
        st.write('## 削除')
        with st.form(key=PAGE + '-delete'):
            user_name = st.selectbox('ユーザ名', users_name.keys())
            is_clicked_delete_button = st.form_submit_button(label='ユーザ削除')

        if is_clicked_delete_button:
            data = {'user_id': users_name[user_name]}
            res = requests.delete(URL_USER, params=data)

            if res.status_code == 200:
                st.success('ユーザ削除完了')
            else:
                st.error('ユーザ削除失敗')
                st.write(res.status_code)
            st.json(res.json())


def main():
    st.title('ユーザ設定画面')

    create_user()
    update_user()
    delete_user()


if __name__ == '__main__':
    main()
