from . import db


class College(db.Model):
    __tablename__ = 'colleges'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), unique=True)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    openid = db.Column(db.String(64), index=True)
    belong_college = db.Column(db.Integer, db.ForeignKey('colleges.id'))
    data = db.Column(db.JSON)
    cookie = db.Column(db.String(128))
