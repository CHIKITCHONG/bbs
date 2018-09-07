from flask import (
    render_template,
    redirect,
    url_for,
    Blueprint,
    send_from_directory
)

from routes import *

from models.topic import Topic
from models.board import Board

main = Blueprint('topic', __name__)


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    bs = Board.all()
    u = current_user()
    ctu = User.one(id=u.id)
    return render_template(
        "topic/index.html",
        ms=ms,
        u=ctu,
        bs=bs,
        bid=board_id
    )


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    # 传递csrf_token到详细页面中
    token = new_csrf_token()
    u = current_user()
    return render_template("topic/detail.html", topic=m, token=token, u=u)


@main.route('/delete/<int:id>')
@login_required
@csrf_required
def delete(id):
    t = Topic.one(id=id)
    u = current_user()
    print('删除 topic 用户是', u, id)
    if t.user_id == u.id:
        Topic.delete(id=t.id)
        return redirect(url_for('.index'))
    else:
        abort(401)


@main.route("/new")
@login_required
def new():
    board_id = int(request.args.get('board_id', -1))
    bs = Board.all()
    token = new_csrf_token()
    # return render_template("topic/new.html", bs=bs, bid=board_id)
    # token = new_csrf_token()
    return render_template(
        "topic/new.html",
        bs=bs,
        bid=board_id,
        token=token
    )


@main.route("/add", methods=["POST"])
@login_required
@csrf_required
def add():
    form = request.form
    u = current_user()
    Topic.new(form, user_id=u.id)
    return redirect(url_for('.index'))


@main.route('/images/<filename>')
def image(filename):
    # 不要直接拼接路由，不安全，比如
    # open(os.path.join('images', filename), 'rb').read()
    return send_from_directory('images', filename)


