# -*- coding: utf-8 -*-
import click
from watchlist import app, db
from watchlist.models import User, Movie


@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database"""
    if drop:
        db.drop_all()  # 删除数据表
    db.create_all()  # 创建数据表
    click.echo('Initialized database.')  # 输出提示信息


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()  # 创建数据表

    # 虚拟电影条目数据
    movies = [
        {
            'title': 'My Neighbor Totoro',
            'year': '1988'
        },
        {
            'title': 'Dead Poets Society',
            'year': '1989'
        },
        {
            'title': 'A Perfect World',
            'year': '1993'
        },
        {
            'title': 'Leon',
            'year': '1994'
        },
        {
            'title': 'Mahjong',
            'year': '1996'
        },
        {
            'title': 'Swallowtail Butterfly',
            'year': '1996'
        },
        {
            'title': 'King of Comedy',
            'year': '1999'
        },
        {
            'title': 'Devils on the Doorstep',
            'year': '1999'
        },
        {
            'title': 'WALL-E',
            'year': '2008'
        },
        {
            'title': 'The Pork of Music',
            'year': '2012'
        },
    ]
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()  # 提交更改
    click.echo('Generate fake data completed!')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()
    user = User.query.first()
    massage = 'Invalid username or password.'
    if user is not None:
        click.echo('Updating user...')
    else:
        user = User()
        click.echo('Creating user...')
    if user.valid_username(username) and user.valid_password(password):
        user.set_name('BL00D')
        user.set_username(username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()  # 提交数据库会话
        massage = 'The superuser definition successful.'
    else:
        massage = 'The superuser definition failed.'
    click.echo(str(massage))
