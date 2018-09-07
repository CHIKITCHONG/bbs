import uuid

import os
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.reply import Reply
from models.topic import Topic
from routes import current_user

from models.user import User


main = Blueprint('setting', __name__)


@main.route("/")
def index():
    # 设置页面
    u = current_user()
    ctu = User.one(id=u.id)
    board_id = int(request.args.get('board_id', -1))
    return render_template("user/setting.html", u=ctu, bid=board_id)


@main.route("/setting/add", methods=['POST'])
def username_add():
    # 更改签名
    form = request.form
    u = current_user()
    ctu = User.one(id=u.id)
    signature = form['sign']
    User.update(u.id, signal=signature)
    return render_template("user/setting.html", u=ctu)


@main.route("/setting/password_add", methods=['POST'])
def pass_add():
    # 更改密码
    form = request.form
    u = current_user()
    ctu = User.one(id=u.id)
    # password = form['pass']
    password = User.salted_password(form['pass'])
    User.update(u.id, password=password)
    return render_template("user/setting.html", u=ctu)


@main.route("/setting/email_add", methods=['POST'])
def email_add():
    # 更改密码
    form = request.form
    u = current_user()
    ctu = User.one(id=u.id)
    # password = form['pass']
    email = form['eamil']
    User.update(u.id, email=email)
    return render_template("user/setting.html", u=ctu)


@main.route('/head_image/add', methods=['POST'])
def head_avatar_add():
    # 更改头像
    file = request.files['avatar']

    # ../../root/.ssh/authorized_keys
    # filename = secure_filename(file.filename)
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    # # 电脑端使用
    # images = 'G:/web2124/images'
    # path = os.path.join(images, filename)

    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('topic.index'))