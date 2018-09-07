from sqlalchemy import create_engine

import secret
from app import configured_app
from models.base_model import db
from models.board import Board
from models.topic import Topic
from models.user import User


def reset_database():
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(secret.database_password)
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS BBS')
        c.execute('CREATE DATABASE BBS CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE BBS')

    db.metadata.create_all(bind=e)


def generate_fake_date():
    form = dict(
        username='test',
        password='123',
    )
    u = User.register(form)

    form = dict(
        title='开发'
    )
    b = Board.new(form)
    form = dict(
        title='测试'
    )
    b = Board.new(form)
    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()
    form = dict(
        title='markdown demo',
        board_id=b.id,
        content=content
    )
    Topic.new(form, u.id)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date()

