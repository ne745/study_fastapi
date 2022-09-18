import datetime
import json

import requests


URL = 'http://localhost:8000/'


def main():
    start_datetime = datetime.datetime.now()
    end_datetime = start_datetime + datetime.timedelta(hours=1)
    booking = {
        'booking_id': 0,
        'user_id': 1,
        'room_id': 2,
        'num_people': 4,
        'start_datetime': start_datetime.isoformat(),
        'end_datetime': end_datetime.isoformat()
    }
    res = requests.post(URL + 'bookings', json.dumps(booking))
    print(res.status_code)
    res = res.json()
    print(res)
    print('=' * 50)

    user = {
        'user_name': 'hoge'
    }
    res = requests.post(URL + 'users', json.dumps(user))
    print(res.status_code)
    res = res.json()
    print(res)

    user = {'user_id': 1}
    res = requests.delete(URL + 'users', params=user)
    print(res.status_code)
    res = res.json()
    print(res)
    print('=' * 50)

    room = {
        'room_id': 0,
        'room_name': 'HOGE room',
        'capacity': 10
    }
    res = requests.post(URL + 'rooms', json.dumps(room))
    print(res.status_code)
    res = res.json()
    print(res)
    print('=' * 50)


if __name__ == '__main__':
    main()
