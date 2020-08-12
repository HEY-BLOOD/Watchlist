# -*- coding: utf-8 -*-
from watchlist import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(300))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值

    def set_name(self, name):
        self.name = name

    def set_username(self, username):
        self.username = username

    def valid_username(self, username):
        valid_length = 0 < len(username) and len(username) <= 20
        ret = valid_length and username.isalnum()  # 内置函数，判断字符串是否只含字母和数字
        return ret

    def valid_password(self, password):
        valid_length = 0 < len(password) and len(password) <= 20
        ret = valid_length and password.isalnum()  # 判断字符串是否为字母和数字组合
        return ret


class Movie(db.Model):  # 表名 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份
