import datetime
import json

import requests


URL = 'http://localhost:8000/'


class TestBooking():
    start_datetime = datetime.datetime.now()
    end_datetime = start_datetime + datetime.timedelta(hours=1)

    def test_create_booking(self):
        user = {
            'user_name': 'test'
        }
        requests.post(URL + 'users', json.dumps(user))
        room = {
            'room_name': 'test room',
            'capacity': 10
        }
        requests.post(URL + 'rooms', json.dumps(room))

        booking = {
            'user_id': 1,
            'room_id': 1,
            'num_people': 5,
            'start_datetime': self.start_datetime.isoformat(),
            'end_datetime': self.end_datetime.isoformat()
        }
        res = requests.post(URL + 'bookings', json.dumps(booking))
        res_json = res.json()
        expected = (
            200,
            1,
            1,
            5,
            self.start_datetime.isoformat(),
            self.end_datetime.isoformat(),
            1,
        )
        actual = (
            res.status_code,
            res_json['user_id'],
            res_json['room_id'],
            res_json['num_people'],
            res_json['start_datetime'],
            res_json['end_datetime'],
            res_json['booking_id'],
        )

        assert expected == actual

    def test_read_booking(self):
        res = requests.get(URL + 'bookings')
        res_json = res.json()
        expected = (
            200,
            1,
            1,
            1,
            5,
            self.start_datetime.isoformat(),
            self.end_datetime.isoformat(),
            1,
        )
        actual = (
            res.status_code,
            len(res_json),
            res_json[0]['user_id'],
            res_json[0]['room_id'],
            res_json[0]['num_people'],
            res_json[0]['start_datetime'],
            res_json[0]['end_datetime'],
            res_json[0]['booking_id'],
        )
        assert expected == actual

    def test_update_booking(self):
        start_datetime = self.start_datetime + datetime.timedelta(days=1)
        end_datetime = self.end_datetime + datetime.timedelta(days=1)
        booking = {
            'user_id': 1,
            'room_id': 1,
            'num_people': 10,
            'start_datetime': start_datetime.isoformat(),
            'end_datetime': end_datetime.isoformat(),
            'booking_id': 1
        }
        res = requests.put(URL + 'bookings', json.dumps(booking))
        res_json = res.json()
        expected = (
            200,
            'success'
        )
        actual = (
            res.status_code,
            res_json['message']
        )
        assert expected == actual

    def test_delete_booking(self):
        booking = {
            'booking_id': 1,
        }
        res = requests.delete(URL + 'bookings', params=booking)
        res_json = res.json()
        expected = (
            200,
            'success'
        )
        actual = (
            res.status_code,
            res_json['message']
        )
        assert expected == actual
