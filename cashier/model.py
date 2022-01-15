from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Cashier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    username = db.Column(db.String(15), unique=True)
    phone_number = db.Column(db.String(13), unique=True)
    email = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    register_date = db.Column(db.DateTime)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method='sha256')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def check_user(user):
        return Cashier.query.filter_by(username=user).first()

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(user_id):
        return Cashier.query.filter_by(id=user_id).first()

    def __repr__(self):
        return '<Cashier: %r>' % self.username