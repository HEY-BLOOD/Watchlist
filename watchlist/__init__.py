# -*- coding: utf-8 -*-
import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

WIN = sys.platform.startswith('win')
if WIN:  # Windows 环境下，三个斜杠
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'

# 把 app.root_path 添加到 os.path.dirname() 中，以便把文件定位到项目根目录
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + \
    os.path.join(os.path.dirname(app.root_path), 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型的修改监控

# 在扩展类实例化前加载配置
db = SQLAlchemy(app)
login_manager = LoginManager(app)  # 实例化扩展类


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    from watchlist.models import User
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


login_manager.login_view = 'login'  # 重定向登录页面
login_manager.login_massage = 'You are not currently logged in, please log in your account first'  # 重定向登录页面提示


@app.context_processor
def inject_vars():  # 函数名可以随意修改
    """模板上下文处理函数"""
    from watchlist.models import User
    user = User.query.first()  # 用户对象
    if not user:
        user.name = 'Blood H'
    return locals()  # 需要返回字典


from watchlist import views, errors, commands