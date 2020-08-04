from os import times
from re import U
from sys import prefix
from flask import Flask, render_template
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import click

app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN:  # Windows 环境下，三个斜杠
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + \
    os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型的修改监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)


class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 用户名


class Movie(db.Model):  # 表名 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


# 自定义创建数据库命令
@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the dataabase"""
    if drop:
        db.drop_all()  # 删除数据表
    db.create_all()  # 创建数据表
    click.echo('Initialized database.')  # 输出提示信息


@app.cli.command()
def forge():
    """Generate fake data."""
    db.drop_all()  # 删除数据表
    db.create_all()  # 创建数据表

    # 全局的两个变量移动到这个函数内
    name = 'Blood H'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit() # 提交更改
    click.echo('Generate fake data completed!')


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    user = User.query.first()  # 读取用户
    if not user:
        user.name = 'Blood'
    movies = Movie.query.all()  # 读取所有电影
    return render_template('index.html', user=user, movies=movies)


@app.route('/user/<name>')
def user_page(name):
    return 'Name: %s ' % name


@app.route('/test')
def test_url_for():
    # 下面是一些调用示例（请在命令行窗口查看输出的 URL）：
    print(url_for('hello'))  # 输出：/home，离视图函数最近的 装饰器
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    print(url_for('user_page', name='peter'))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'
