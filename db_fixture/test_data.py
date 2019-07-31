import sys
from django.test import TestCase

sys.path.append('../db_fixture')
from db_fixture.mysql_db import DB

# 发布会表数据
datas = {'sign_event':
    [
        {'id': 4, 'name': 'red rice 4', 'limit': 2000, 'status': 1, 'address': 'beijing',
         'start_time': '2019-09-30 18:00:00'},
        {'id': 5, 'name': '可参加人数为0', 'limit': 0, 'status': 1, 'address': 'beijing',
         'start_time': '2019-09-30 18:00:00'},
        {'id': 6, 'name': '当前状态为0关闭', 'limit': 2000, 'status': 0, 'address': 'beijing',
         'start_time': '2019-09-30 18:00:00'},
        {'id': 7, 'name': '发布会已结束', 'limit': 2000, 'status': 1, 'address': 'beijing',
         'start_time': '2018-09-30 18:00:00'},
        {'id': 8, 'name': 'red rice 5', 'limit': 2000, 'status': 1, 'address': 'beijing',
         'start_time': '2018-09-30 18:00:00'}
    ],
    'sign_guest': [
        {'id': 3, 'realname': 'lily3', 'phone': '13568821400', 'email': 'lily3@email.com', 'sign': 0, 'event_id': 1},
        {'id': 4, 'realname': 'lily4', 'phone': '13568821404', 'email': 'lily4@email.com', 'sign': 1, 'event_id': 1},
        {'id': 5, 'realname': 'lily5', 'phone': '13568821405', 'email': 'lily5@email.com', 'sign': 0, 'event_id': 5},

    ]
}


def init_data():
    db = DB()
    for table, data in datas.items():
        # db.clear(table)
        for d in data:
            db.insert(table, d)
    db.close()


class TestData(TestCase):

    def test_insert_data(self):
        init_data()
