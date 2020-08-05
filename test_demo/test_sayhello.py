import unittest
from module_foo import sayhello


class SayHelloTestCase(unittest.TestCase):
    """测试用例"""

    def setUp(self):
        """测试固件，每个测试方法执行前被调用"""
        pass

    def tearDown(self):
        """测试固件，每个测试方法执行后被调用"""
        pass

    def test_sayhello(self):  # 第 1 个测试方法
        rv = sayhello()
        self.assertEqual(rv, 'Hello!')

    def test_sayhello_to_somebody(self):  # 第 2 个测试方法
        rv = sayhello(to='Blood')
        self.assertEqual(rv, 'Hello, Blood!')


if __name__ == "__main__":
    unittest.main()
