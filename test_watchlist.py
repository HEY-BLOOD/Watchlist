import unittest
from watchlist import app, db
from watchlist.models import User, Movie
from watchlist.commands import initdb, forge


class WatchlistTestCase(unittest.TestCase):
    """ watchlist 程序测试"""

    def setUp(self):
        # 更新配置
        app.config.update(
            TESTING=True,  # 开启测试模式，在出错时不会输出多余信息
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'  # 使用 SQLite 内存型数据库
        )
        # 创建数据库和表
        db.create_all()
        # 创建测试数据，一个用户，一个电影条目
        user = User(name='TestName', username='TestUsername')
        user.set_password('TestPassword')
        movie = Movie(title='Test Movie Title', year='2019')
        # 使用 add_all() 方法一次添加多个模型类实例，传入列表
        db.session.add_all([user, movie])
        db.session.commit()
        self.client = app.test_client()  # 创建测试客户端
        self.runner = app.test_cli_runner()  # 创建测试命令运行器

    def tearDown(self):
        db.session.remove()  # 清除数据库会话
        db.drop_all()  # 删除数据库表

    def test_app_exist(self):
        """ 测试程序实例是否存在 """
        self.assertIsNotNone(app)

    def test_app_is_testing(self):
        """ 测试程序是否处于测试模式 """
        self.assertTrue(app.config['TESTING'])

    def test_404_page(self):
        """ Page not fount Test Function """
        response = self.client.get('/nothing')  # Get 方法访问 URL 路由
        data = response.get_data(as_text=True)  # 获取 Unicode 格式的响应主体
        self.assertIn('Page Not Found - 404', data)  # 判断是否包含预期值
        self.assertIn('Go Home', data)
        self.assertEqual(response.status_code, 404)  # 判断响应状态码

    def test_index_page(self):
        """ Home page Test Function """
        response = self.client.get('/')  # Get 方法访问 '/' 路由
        data = response.get_data(as_text=True)
        self.assertIn('TestName\'s Watchlist', data)
        self.assertIn('Test Movie Title', data)
        self.assertEqual(response.status_code, 200)

    def login(self):
        """ 辅助方法，用于登入用户 """
        self.client.post('/login', data=dict(  # Post 方法，发送请求，登录账户
            username='TestUsername',
            password='TestPassword'
        ), follow_redirects=True)  # 跟随重定向

    def test_add_item(self):
        ''' 测试创建条目 '''
        self.login()  # 首先在客户端登录用户

        # 测试创建条目操作
        response = self.client.post(
            '/', data=dict(title='New Movie', year='2019'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item created.', data)  # 创建成功提示
        self.assertIn('New Movie', data)  # 新条目的名称

        # 测试创建条目操作，电影标题 title 为空
        response = self.client.post(
            '/', data=dict(title='', year='2019'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item created.', data)  # 没有创建成功提示
        self.assertIn('Invalid input.', data)  # 输入不合法

        # 测试创建条目操作，电影年份 year 为空
        response = self.client.post(
            '/', data=dict(title='New Movie', year=''), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item created.', data)  # 没有创建成功提示
        self.assertIn('Invalid input.', data)  # 输入不合法

    def test_update_item(self):
        """ 测试更新条目 """
        self.login()  # 首先在客户端登录用户

        # 测试更新条目页面
        response = self.client.get('/movie/edit/1')
        data = response.get_data(as_text=True)
        self.assertIn('Test Movie Title', data)
        self.assertIn('2019', data)

        # 测试更新条目操作
        response = self.client.post(
            '/movie/edit/1', data=dict(title='New Movie Edited', year='2019'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item updated.', data)
        self.assertNotIn('Invalid input.', data)

        # 测试更新条目操作，电影标题 title 为空
        response = self.client.post(
            '/movie/edit/1', data=dict(title='', year='2019'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item updated.', data)
        self.assertIn('Invalid input.', data)
        self.assertNotIn('Test Movie Title', data)  # 显示条目 1 的原标题

        # 测试更新条目操作，电影年份 year 为空
        response = self.client.post(
            '/movie/edit/1', data=dict(title='New Movie Edited Again', year=''), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item updated.', data)
        self.assertIn('Invalid input.', data)
        self.assertNotIn('Test Movie Title', data)  # 显示条目 1 的原标题
        self.assertNotIn('New Movie Edited Again', data)

    def test_delete_item(self):
        """ 测试删除条目 """
        self.login()  # 首先在客户端登录用户

        # 测试删除条目
        response = self.client.post('/movie/delete/1', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item deleted.', data)
        self.assertNotIn('Test Movie Title', data)

    def test_login_protect(self):
        """ 测试登录保护 """
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('Login', data)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('<form method="post">', data)

    def test_login(self):
        """ 测试用户登录 """

        # 测试登录
        response = self.client.post(
            '/login', data=dict(username='TestUsername', password='TestPassword'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('TestName', data)
        self.assertIn('Edit', data)
        self.assertIn('Delete', data)
        self.assertIn('Settings', data)
        self.assertIn('Logout', data)
        self.assertIn('Login success.', data)  # 已经有 Login 字符串
        self.assertNotIn('<a href="/login">Login</a>', data)  # Login 超链接
        self.assertNotIn('Invalid input.', data)
        self.assertNotIn('Invalid username or password.', data)
        self.client.get('/logout')  # 退出登录

        # 测试使用错误的密码登录
        response = self.client.post(
            '/login', data=dict(username='TestUsername', password='TestInvalidPassword'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Login success.', data)
        self.assertNotIn('Invalid input.', data)
        self.assertIn('<h3>Login</h3>', data)
        self.assertIn('TestName', data)
        self.assertIn('<h3>Login</h3>', data)
        self.assertIn('Invalid username or password.', data)

        # 测试使用错误的用户名登录
        response = self.client.post(
            '/login', data=dict(username='TestInvalidUsername', password='TestPassword'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Login success.', data)
        self.assertNotIn('Invalid input.', data)
        self.assertIn('<h3>Login</h3>', data)
        self.assertIn('TestName', data)
        self.assertIn('Login', data)
        self.assertIn('Invalid username or password.', data)

        # 测试使用错误的密码和错误的用户名登录
        response = self.client.post(
            '/login', data=dict(username='TestInvalidUsername', password='TestInvalidPassword'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Login success.', data)
        self.assertNotIn('Invalid input.', data)
        self.assertIn('<h3>Login</h3>', data)
        self.assertIn('TestName', data)
        self.assertIn('Login', data)
        self.assertIn('Invalid username or password.', data)

        # 测试使用空密码登录
        response = self.client.post(
            '/login', data=dict(username='TestUsername', password=''), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Login success.', data)
        self.assertNotIn('Invalid username or password.', data)
        self.assertIn('Invalid input.', data)
        self.assertIn('TestName', data)
        self.assertIn('Login', data)
        self.assertIn('<h3>Login</h3>', data)

        # 测试使用空用户名登录
        response = self.client.post(
            '/login', data=dict(username='TestUsername', password=''), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Login success.', data)
        self.assertNotIn('Invalid username or password.', data)
        self.assertIn('Invalid input.', data)
        self.assertIn('TestName', data)
        self.assertIn('Login', data)
        self.assertIn('<h3>Login</h3>', data)

        # 测试使用空密码和空用户名登录
        response = self.client.post(
            '/login', data=dict(username='TestUsername', password=''), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Login success.', data)
        self.assertNotIn('Invalid username or password.', data)
        self.assertIn('Invalid input.', data)
        self.assertIn('TestName', data)
        self.assertIn('Login', data)
        self.assertIn('<h3>Login</h3>', data)

    def test_logout(self):
        """ 测试登出 """
        self.login()  # 首先在客户端登录用户

        response = self.client.get('/logout', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Goodbye.', data)
        self.assertIn('Login', data)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('<form method="post">', data)
        self.assertNotIn('<h3>Login</h3>', data)

    def test_settings(self):
        """ 测试设置 """
        self.login()  # 首先在客户端登录用户

        # 测试设置页面
        response = self.client.get('/settings', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('<h3>Settings</h3>', data)
        self.assertIn('Your Name', data)

        # 测试更新设置
        response = self.client.post('/settings', data=dict(
            name='Blood Wong',
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Settings updated.', data)
        self.assertIn('Blood Wong', data)

        # 测试更新设置，姓名为空
        response = self.client.post('/settings', data=dict(
            name='',
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Blood Wong', data)  # 上面更新成功后的名称
        self.assertIn('Invalid input.', data)
        self.assertNotIn('Settings updated.', data)

    def test_forge_command(self):
        """ 测试 forge 命令，创建虚拟数据 """
        result = self.runner.invoke(forge)  # 在控制台执行 forge 命令
        self.assertIn('Generate fake data completed!',
                      result.output)  # 比较执行命令后的输出

    def test_initdb_command(self):
        """ 测试 initdb 命令，初始化数据库 """

        # 初始化数据库，无参数
        result = self.runner.invoke(initdb)
        self.assertIn('Initialized database.', result.output)

        # 初始化数据库，参数 --drop
        result = self.runner.invoke(args=['initdb', '--drop'])
        self.assertIn('Initialized database.', result.output)

    def test_admin_command(self):
        """ 测试 admin 命令，生成管理员用户 """

        # 没有创建过管理员用户
        self.runner.invoke(args=['initdb', '--drop'])  # 初始化数据库，删除 setUp中创建的用户
        result = self.runner.invoke(
            args=['admin', '--username', 'admin_username', '--password', 'admin_password'])
        self.assertIn('Creating user...', result.output)
        self.assertIn('Completed.', result.output)
        self.assertEqual(User.query.count(), 1)  # 唯一的管理员用户
        self.assertEqual(User.query.first().username, 'admin_username')
        self.assertTrue(User.query.first().validate_password('admin_password'))

        # 已经创建过管理员用户
        result = self.runner.invoke(
            args=['admin', '--username', 'admin_username_again', '--password', 'admin_password_again'])
        self.assertIn('Updating user...', result.output)
        self.assertIn('Completed.', result.output)
        self.assertEqual(User.query.count(), 1)  # 唯一的管理员用户
        self.assertEqual(User.query.first().username, 'admin_username_again')
        self.assertTrue(User.query.first().validate_password(
            'admin_password_again'))

    def test_admin_command_update(self):
        """ 测试更新管理员账户 """
        # 使用 args 参数给出完整的命令参数列表
        result = self.runner.invoke(args=['admin', '--username',
                                          'peter', '--password', 'updated_password'])
        self.assertIn('Updating user...', result.output)
        self.assertIn('Completed.', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'peter')
        self.assertTrue(
            User.query.first().validate_password('updated_password'))


if __name__ == "__main__":
    unittest.main()
