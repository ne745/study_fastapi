import streamlit as st

from pages.booking import read_booking, generate_booking_table


st.title('会議室予約システム')

st.write('### 予約一覧')
bookings = read_booking()
if bookings:
    df_bookings_ja = generate_booking_table()
    st.table(df_bookings_ja)
else:
    st.write('現在予約はありません')
