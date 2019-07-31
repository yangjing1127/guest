import pymysql
from pymysql.err import OperationalError
import os
import configparser as cparser

# 读取db_config的配置
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
print(base_dir)
file_path = base_dir + "/db_config.ini"
print(file_path)
cf = cparser.ConfigParser()
cf.read(file_path)
print(cf.sections())
host = cf.get("mysqlconf", "host")
port = cf.get("mysqlconf", "port")
db = cf.get("mysqlconf", "db_name")
user = cf.get("mysqlconf", "user")
password = cf.get("mysqlconf", "password")
print(host)


# 封装mysql基本操作
class DB:

    def __init__(self):
        try:
            # 连接数据库
            self.conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4',
                                        cursorclass=pymysql.cursors.DictCursor)

        except OperationalError as e:
            print("Mysql Error %d:%s" % (e.args[0], e.args[1]))

    # 清除表数据
    def clear(self, table_name):
        real_sql = "delete from " + table_name + ";"
        with self.conn.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
            self.conn.commit()

    # 插入表数据
    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'" + str(table_data[key]) + "'"
            key = ','.join(table_data.keys())
            print(key)
            table_datas = table_data.values()
            value = ','.join('%s' % data for data in table_datas)
            # 解决expected str instance, int found
            print(value)
            real_sql = "Insert into " + table_name + "(" + key + ") values" + "(" + value + ")"
            print(real_sql)
        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)
        self.conn.commit()
        # 关闭数据连接

    def close(self):
        self.conn.close()

    # if __name__ == '__main__':
    #     db = DB()
    #     table_name = "sign_event"
    #     data = {
    #         'id': 4, 'name': 'red rice 4', 'limit': 2000, 'status': 1, 'address': 'beijing',
    #         'start_time': '2019-09-30 18:00:00',
    #         'id': 5, 'name': 'red rice 5', 'limit': 2000, 'status': 1, 'address': 'beijing',
    #         'start_time': '2019-09-30 18:00:00',
    #
    #     }
    #     db.insert(table_name,data)
    #     db.close()
