from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.reply import Reply
from models.topic import Topic
from routes import *

from models.user import User


main = Blueprint('gua_user', __name__)


@main.route("/")
@login_required
def index():
    pass