from flask import Flask

from App.config import envs, basedir
from App.ext import init_ext
from App import models
from App.views import init_first_blue


def create_app():

    # 初始化app
    app = Flask(__name__, template_folder="../templates")

    # 初始化配置文件settings
    app.config.from_object(envs.get('develop'))

    # 初始化蓝图、路由
    init_first_blue(app)

    # 初始化第三方库
    init_ext(app)

    return app

