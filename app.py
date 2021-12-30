
from flask import Flask, render_template
from sqlalchemy.orm import relationship

from database import db
from os import urandom
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mobility import Mobility
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)


# def create_app():
#     app = Flask(__name__)
#     app.secret_key = urandom(24)
#     app.config.from_pyfile('config.cfg')
#     db.init_app(app)
#     with app.test_request_context():
#         db.create_all()
#     return app
class Cashier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    phone_number = db.Column(db.String(13), unique=True)
    email = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    register_date = db.Column(db.DateTime)
    receipts = db.relationship('Receipt', backref='receipt', lazy='dynamic')

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

    def __repr__(self):
        return '<Member: %r>' % self.username


class Menuitem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(32), unique=True)
    price = db.Column(db.Integer)
    discount = db.Column(db.Integer)
    serving_time_period = db.Column(db.String(16))
    estimated_cooking_time = db.Column(db.Time)
    is_delete = db.Column(db.Boolean, default=False)
    item_category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    orders = db.relationship('Order', backref='menuitem')
    # orders = relationship("Order")

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def find_item(item_name):
        return MenuItem.query.filter_by(item_name=item_name).first()

    def __repr__(self):
        return '<word: %r>' % self.word


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(32), unique=True)
    table_number = db.Column(db.Integer, unique=True)
    cafe_space_position = db.Column(db.String(16), unique=True)
    receipts = db.relationship('Receipt', backref='table', lazy='dynamic')
    orders = db.relationship('Order', backref='table', lazy='dynamic')

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def find_table(id):
        return Table.query.filter_by(id=id).first()

    def __repr__(self):
        return '<table number: %r>' % self.id


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menuitem.id'))
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    item_count = db.Column(db.SmallInteger, primary_key=True)
    status = db.Column(db.String(32), default='waiting')
    submit_time = db.Column(db.DateTime)
    is_delete = db.Column(db.Boolean, default=False)

    @staticmethod
    def find_orders(table_id):
        return Table.query.filter_by(table_id=table_id).all()

    def create(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<table number: %r>' % self.id


class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orders = db.Column(db.PickleType)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    time_stamp = db.Column(db.DateTime)
    cashier_id = db.Column(db.Integer, db.ForeignKey('cashier.id'))
    pay_status = db.Column(db.Boolean, default=False)
    total_price = db.Column(db.Integer)
    final_price = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def final_receipt(table_id):
        return Receipt.query.filter_by(table_id=table_id).first()

    def __repr__(self):
        return '<word: %r>' % self.word


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32), unique=True)
    duration = db.Column(db.String(32))
    menu_item = db.relationship('MenuItem', backref='menuitem', lazy='dynamic')

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def find_category(id):
        return Category.query.filter_by(id=id).first()

    def __repr__(self):
        return '<table number: %r>' % self.id


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
