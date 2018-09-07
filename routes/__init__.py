import uuid
from functools import wraps

from flask import session, request, abort, redirect, url_for

from models.user import User
from models.token import Token


def current_user():
    uid = session.get('user_id', '')
    u = User.one(id=uid)
    return u


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'token' in request.form:
            token = request.form['token']
        else:
            token = request.args['token']
        u = current_user()
        t = Token.one(content=token)
        # 判断是否是这个用户生成的token
        if t is not None and (t.user_id is None or t.user_id == u.id):
            Token.delete(content=token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    if u:
        form = dict(
            content=token,
            user_id=u.id
        )
    else:
        form = dict(
            content=token,
        )
    Token.new(form)
    return token


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user():
            return f(*args, **kwargs)
        else:
            return redirect(url_for('index.signin'))
    return wrapper