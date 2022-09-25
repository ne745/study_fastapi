import json

import requests


URL = 'http://localhost:8000/'


class TestRoom():
    def test_create_room(self):
        room = {
            'room_name': 'test',
            'capacity': 10
        }
        res = requests.post(URL + 'rooms', json.dumps(room))
        res_json = res.json()
        expected = (
            200,
            1,
            'test',
            10
        )
        actual = (
            res.status_code,
            res_json['room_id'],
            res_json['room_name'],
            res_json['capacity']
        )
        assert expected == actual

    def test_read_room(self):
        res = requests.get(URL + 'rooms')
        res_json = res.json()
        expected = (
            200,
            1,
            1,
            'test'
        )
        actual = (
            res.status_code,
            len(res_json),
            res_json[0]['room_id'],
            res_json[0]['room_name'],
        )
        assert expected == actual

    def test_update_room(self):
        room = {
            'room_id': 1,
            'room_name': 'testtest',
            'capacity': 100
        }
        res = requests.put(URL + 'rooms', json.dumps(room))
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

    def test_delete_room(self):
        room = {
            'room_id': 1,
        }
        res = requests.delete(URL + 'rooms', params=room)
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
