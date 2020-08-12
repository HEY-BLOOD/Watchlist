# -*- coding: utf-8 -*-
from watchlist import app
from flask import render_template
from werkzeug.exceptions import HTTPException


@app.errorhandler(Exception)
def all_exception_handler(e):
    """ 处理所有的 HTTP 错误 """
    # 对于 HTTP 异常，返回自带的错误描述和状态码
    # 这些异常类在 Werkzeug 中定义，均继承 HTTPException 类# 500 未知异常
    result = render_template('error.html',
                             description='Sorry, internal error.'), 500
    if isinstance(e, HTTPException):
        result = render_template('error.html',
                                 description=e.description), e.code
    return result  # 返回响应和 状态码
