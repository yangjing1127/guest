from django.test import TestCase
from sign.models import Event, Guest
from django.contrib.auth.models import User


# 更多django 测试参考官方文档
# https://docs.djangoproject.com/en/1.10/topics/testing
class GuestManageTest(TestCase):
    '''嘉宾管理测试类'''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.cocm', 'admin123456', '')
        Event.objects.create(name="xiaomi5", limit=2000, address='beijing',
                             status=1, start_time='2019-09-01 18:00:00')
        Guest.objects.create(realname="alen", phone="188888888", email="alan@mail.com", sign=0, event_id=1)
        self.login_user = {'username': 'admin', 'password': 'admin123456'}

    def test_guest_manage_success(self):
        '''测试嘉宾信息'''
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alen", response.content)
        self.assertIn(b"18888888", response.content)

    def test_guest_manage_search_success(self):
        '''测试时嘉宾搜索功能'''
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_phone/', {"phone": "18888888"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alen", response.content)
        self.assertIn(b"18888888", response.content)


class EventManageTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.cocm', 'admin123456', '')
        Event.objects.create(name="xiaomi5", limit=2000, address='beijing',
                             status=1, start_time='2019-09-01 18:00:00')
        self.login_user = {'username': 'admin', 'password': 'admin123456'}

    def test_event_manage_success(self):
        '''测试发布会：xiaomi5'''
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/event/manage')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)

    def test_event_manage_search_success(self):
        '''测试发布会搜索'''
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_name/', {"name": "xiaomi5"})
        self.assertEqual(response.status_code)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)


class LoginActionTest(TestCase):
    '''测试登录动作'''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.cocm', 'admin123456', '')

    def test_add_admin(self):
        '''测试添加用户'''
        user = User.objects.get(username="admin")
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@mail.com")

    def test_login_action_username_password_null(self):
        '''用户密码为空'''
        test_data = {'username': '', 'passsword': ''}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error", response.content)

    def test_login_action_username_password_error(self):
        '''用户密码错误'''
        test_data = {'username': 'abc', 'password': '123'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)
        # 断言html页面是否包含“username or password error!”字符串

    def test_login_action_success(self):
        '''登录成功'''
        test_data = {'username': 'admin', 'password': 'admin123456'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)


class ModuleTest(TestCase):
    def setUp(self):
        # 初始化变量，生成数据库测试数据、打开浏览器
        Event.objects.create(id=1, name='oneplus 3 event', status=True, limit=2000,
                             address='shenzhen', start_time='2019-08-31 14:00:00')
        Guest.objects.create(id=1, event_id=1, realname='yangjing', phone='15868821400',
                             email='yangjing@12.com', sign=False)

    def tearDown(self):
        # 清除数据库测试数据、关闭文件、关闭浏览器
        pass

    def test_event_models(self):
        result = Event.objects.get(name="oneplus 3 event")
        self.assertEqual(result.address, "shenzhen")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='15868821400')
        self.assertEqual(result.realname, 'yangjing', "姓名不一致")
        self.assertFalse(result.sign)
