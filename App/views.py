import os

from flask import render_template, flash, redirect, g, url_for, session, request, Blueprint
from flask_login import login_user, current_user, login_required
from flask_openid import OpenID

from App import basedir
from App.ext import lm, db
from App.forms import LoginForm
from App.models import User
from App.config import Config
from flask import current_app as app
from flask import Blueprint

blue = Blueprint('first_blue', __name__)


def init_first_blue(app):
    app.register_blueprint(blueprint=blue)


def login_handler(func):
    def wrapper(*args, **kwargs):
        g.oid.loginhandler(func)
        return func(*args, **kwargs, oid=g.oid)

    return wrapper


def after_login(func):
    def wrapper(*args, **kwargs):
        g.oid.after_login(func)
        return func(*args, **kwargs, oid=g.oid)

    return wrapper


@blue.route('/')
@blue.route('/index')
@login_required
def index():
    user = g.user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title='Home', user=user, posts=posts)


@blue.route('/login', methods=['GET', 'POST'])
@login_handler  # 不懂啥意思 我们在视图函数上添加一个新的装饰器。oid.loginhandle 告诉 Flask-OpenID 这是我们的登录视图函数。
def login(oid):
    if g.user is not None and g.user.is_authenticated:  # Flask 中的 g 全局变量是一个在请求生命周期中用来存储和共享数据。我敢肯定你猜到了，我们将登录的用户存储在这里(g)。
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        # return redirect('/index')
        session[
            'remember_me'] = form.remember_me.data  # 当我们从登录表单获取的数据后的处理代码也是新的。这里我们做了两件事。首先，我们把 remember_me 布尔值存储到 flask 的会话中，这里别与 Flask-SQLAlchemy 中的 db.session 弄混淆。之前我们已经知道 flask.g 对象在请求整个生命周期中存储和共享数据。flask.session 提供了一个更加复杂的服务对于存储和共享数据。一旦数据存储在会话对象中，在来自同一客户端的现在和任何以后的请求都是可用的。数据保持在会话中直到会话被明确地删除。为了实现这个，Flask 为我们应用程序中每一个客户端设置不同的会话文件。
        return oid.try_login(form.openid.data, ask_for=['nickname',
                                                        'email'])  # id.try_login 被调用是为了触发用户使用 Flask-OpenID 认证。该函数有两个参数，用户在 web 表单提供的 openid 以及我们从 OpenID 提供商得到的数据项列表。因为我们已经在用户模型类中定义了 nickname 和 email，这也是我们将要从 OpenID 提供商索取的。
    return render_template('login.html', title='Sign In', form=form,
                           providers=Config.OPENID_PROVIDERS)  # OpenID 认证异步发生。如果认证成功的话，Flask-OpenID 将会调用一个注册了 oid.after_login 装饰器的函数。如果失败的话，用户将会回到登陆页面。


@lm.user_loader  # 不懂啥意思
def load_user(id):
    return User.query.get(int(id))


@after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@blue.before_request
def before_request():
    g.user = current_user
    g.oid = OpenID(app, os.path.join(basedir, 'tmp'))
