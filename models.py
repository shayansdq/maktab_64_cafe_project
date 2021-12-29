from database import db
# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime


class Cashier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
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

    def __repr__(self):
        return '<Member: %r>' % self.username


class MenuItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(32))
    price = db.Column(db.Integer)
    item_category = db.Column(db.Integer, db.ForeignKey('category.id'))
    discount = db.Column(db.Integer)
    serving_time_period = db.Column(db.String(16))
    estimated_cooking_time = db.Column(db.Time)
    is_delete = db.Column(db.Boolean, default=False)

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def find_card(id):
        return MenuItems.query.filter_by(id=id).first()

    def __repr__(self):
        return '<word: %r>' % self.word


class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orders = db.Column(db.PickleType)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    total_price = db.Column(db.Integer)
    time_stamp = db.Column(db.DateTime)
    cashier_id = db.Column(db.Integer, db.ForeignKey('chashier.id'))

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def final_receipt(table_id):
        return Receipt.query.filter_by(table_id=table_id).first()

    def __repr__(self):
        return '<word: %r>' % self.word


class Tables(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(32), unique=True)
    table_number = db.Column(db.Integer, unique=True)
    cafe_space_position = db.Column(db.String(16), unique=True)

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def find_table(id):
        return Tables.query.filter_by(id=id).first()

    def __repr__(self):
        return '<table number: %r>' % self.id
