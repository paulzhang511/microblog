from App.ext import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def is_authenticated(self):  # 被认证的
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):  # 是否匿名
        return False

    def get_id(self):
        # try:
        #     return unicode(self.id)  # python2
        # except NameError:
        # get_id 方法应该返回一个用户唯一的标识符，以 unicode 格式。我们使用数据库生成的唯一的 id。需要注意地是在 Python 2 和 3 之间由于 unicode 处理的方式的不同我们提供了相应的方式。
        return str(self.id)  # python3

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

