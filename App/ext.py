from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
lm = LoginManager()


def init_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    lm.init_app(app)
    lm.login_view = 'login'

