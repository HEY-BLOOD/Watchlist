# -*- coding: utf-8 -*-
from watchlist import app
from flask import render_template


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    """Custom 404 Errors page"""
    response = render_template('errors/404.html')
    return response, 404  # 返回响应和状态码
