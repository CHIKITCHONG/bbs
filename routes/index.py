import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    abort,
    send_from_directory
)
from werkzeug.utils import secure_filename

from models.reply import Reply
from models.user import User
from routes import current_user
from models.topic import Topic
from utils import log
from models.board import Board

main = Blueprint('index', __name__)


@main.route("/")
def index():
    # u = current_user()
    # # return render_template("index.html", user=u)
    # return render_template("topic/index.html", user=u)
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    bs = Board.all()
    u = current_user()
    if u is None:
        return render_template("topic/index.html", ms=ms, u=u, bs=bs, bid=board_id)
    else:
        ctu = User.one(id=u.id)
    return render_template("topic/index.html", ms=ms, u=ctu, bs=bs, bid=board_id)


@main.route("/signin", methods=['GET'])
def signin():
    return render_template('loginout/signin.html')


@main.route("/signup", methods=['GET'])
def signup():
    return render_template('loginout/signup.html')


@main.route("/register", methods=['POST'])
def register():
    form = request.form.to_dict()
    # 用类函数来判断
    u = User.register(form)
    if u is None:
        flag = False
        return render_template("loginout/signup.html", flag=flag)
    else:
        # 设置session以获得登录状态
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        flag = False
        return render_template(
            'loginout/signin.html',
            flag=flag,
        )
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        # 转到 topic.index 页面
        return redirect(url_for('topic.index'))


@main.route('/signout', methods=['GET'])
def signout():
    session.pop('user_id')
    return redirect('/')


@main.route('/user/<int:id>')
def user_detail(id):
    u = User.one(id=id)
    if u is None:
        abort(404)
    else:
        # return render_template('profile.html', user=u)
        # 最近创建的话题
        ustp = Topic.all(user_id=u.id)
        ustp.reverse()
        # 最近回复过的话题
        usrp = Reply.all(user_id=u.id)
        title_list = []

        for i in usrp:
            title_list.append(Topic.one(id=i.topic_id))
        usrp = [c.__dict__ for c in title_list]
        usrp.reverse()

        return render_template("user/index.html", ustp=ustp, usrp=usrp, u=u)


@main.route('/about', methods=['GET'])
def about():
    u = current_user()
    return render_template(
        'topic/about.html',
        u=u,
    )


@main.route('/image/add', methods=['POST'])
def avatar_add():
    file = request.files['avatar']
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)
    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('.profile'))


@main.route('/images/<filename>')
def image(filename):
    # 不要直接拼接路由，不安全，比如
    # open(os.path.join('images', filename), 'rb').read()
    return send_from_directory('images', filename)