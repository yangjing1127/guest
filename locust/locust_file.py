from locust import HttpLocust, TaskSet, task

# 定义用户行为
'''
locust -f locust_file.py --host=https://www.baidu.com

locust -f locust_file.py --host=https://www.baidu.com --no-web -c 10 -r 10 -n 3000
--no-web 表示不使用web界面运行测试
-c 设置虚拟用户数
-r 设置每秒启动虚拟用户数
-n 设置请求个数

系统瓶颈在数据库读写上时，有效手段使用redis缓存处理，减少数据库读写频率
'''


class UserBehavior(TaskSet):
    @task
    def baidu_page(self):
        self.client.get("/")


class WebSiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 6000
