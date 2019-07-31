import unittest

from sign.module import Calculator


# Create your tests here.

class ModuleTest(unittest.TestCase):
    def setUp(self):
        # 初始化变量，生成数据库测试数据、打开浏览器
        self.cal = Calculator(8, 4)

    def tearDown(self):
        # 清除数据库测试数据、关闭文件、关闭浏览器
        pass

    def test_add(self):
        result = self.cal.add()
        self.assertEqual(result, 12)

    def test_sub(self):
        result = self.cal.sub()
        self.assertEqual(result, 4)

    def test_mul(self):
        result = self.cal.mul()
        self.assertEqual(result, 32)

    def test_div(self):
        result = self.cal.div()
        self.assertEqual(result, 2)


if __name__ == "__main__":
    # unittest.main()
    # 构造测试集合
    suite = unittest.TestSuite()
    suite.addTest(ModuleTest("test_add"))
    suite.addTest(ModuleTest("test_sub"))
    suite.addTest(ModuleTest("test_mul"))
    suite.addTest(ModuleTest("test_div"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
