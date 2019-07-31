import requests
import unittest


class GetEventListTest(unittest.TestCase):
    # 查询发布会接口
    def setUp(self):
        self.url = "http://127.0.0.1:8000/api/get_event_list/"

    def test_get_event_null(self):
        '''发布会id为空'''
        r = requests.get(self.url, params={'eid': ''})
        result = r.json()
        print(result)
        print(result['status'])
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], "parameter error")

    # def test_get_event_error(self):
    #     '''发布会id不存在'''
    #     r = requests.get(self.url, params={'eid': '123'})
    #     result = r.json()
    #     print(result)
    #     print(result['status'])
    #     self.assertEqual(result['status'], 10022)
    #     self.assertEqual(result['message'], "parameter error")

    # def test_get_event_success(self):
    #     '''发布会id=1'''
    #     r = requests.get(self.url, params={'eid': '1'})
    #     result = r.json()
    #     print(result)
    #     print(result['status'])
    #     self.assertEqual(result['status'], 200)
    #     self.assertEqual(result['message'], "success")


if __name__ == '__main__':
    unittest.main()
