from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    belong_college = db.Column(db.Integer, db.ForeignKey('colleges.id'))
    name = db.Column(db.String(12))
    Sno = db.Column(db.String(12))
    pic = db.Column(db.Text)
    ehall_cookie = db.Column(db.JSON)
    ecard_cookie = db.Column(db.JSON)
    ehall_password = db.Column(db.String(128))
    ecard_password = db.Column(db.String(128))
    data = db.Column(db.JSON)


class College(db.Model):
    __tablename__ = 'colleges'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship(User, backref='college')
    times = db.Column(db.BigInteger)
