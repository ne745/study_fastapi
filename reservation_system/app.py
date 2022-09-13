import json
import random

import requests
import streamlit as st


URL = 'http://localhost:8000'


st.title('API テスト画面 (ユーザ)')
with st.form(key='user'):
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
