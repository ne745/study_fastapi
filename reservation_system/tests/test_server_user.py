import json

import requests


URL = 'http://localhost:8000/'


class TestUser():
    def test_create_user(self):
        user = {
            'user_name': 'test'
        }
        res = requests.post(URL + 'users', json.dumps(user))
        res_json = res.json()
        expected = (
            200,
            1,
            'test'
        )
        actual = (
            res.status_code,
            res_json['user_id'],
            res_json['user_name'],
        )
        assert expected == actual

    def test_read_user(self):
        res = requests.get(URL + 'users')
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
            res_json[0]['user_id'],
            res_json[0]['user_name'],
        )
        assert expected == actual

    def test_update_user(self):
        user = {
            'user_id': 1,
            'user_name': 'testtest'
        }
        res = requests.put(URL + 'users', json.dumps(user))
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

    def test_delete_user(self):
        user = {
            'user_id': 1,
        }
        res = requests.delete(URL + 'users', params=user)
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
