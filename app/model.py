from app import db


class College(db.Model):
    __tablename__ = 'colleges'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='colleges')
    times = db.Column(db.BigInteger)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    belong_college = db.Column(db.Integer, db.ForeignKey('colleges.id'))
    Sno = db.Column(db.String(12))
    data = db.Column(db.JSON)
