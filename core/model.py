from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, unique=True)
    menuitems = db.relationship('Menuitem', backref='discount', lazy='dynamic')

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_val(value):
        return Discount.query.filter_by(value=value).first().id


class Menuitem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(32))
    price = db.Column(db.Integer)
    serving_time_period = db.Column(db.String(16))
    estimated_cooking_time = db.Column(db.Time)
    is_delete = db.Column(db.Boolean, default=False)
    item_category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    orders = db.relationship('Order', backref='menuitem')
    discount_id = db.Column(db.Integer, db.ForeignKey('discount.id'))

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(item_id):
        return Menuitem.query.filter_by(id=item_id).first()

    @staticmethod
    def get_valid_items():
        return Menuitem.query.filter_by(is_delete=False).all()

    @staticmethod
    def find_item(item_name):
        return Menuitem.query.filter_by(item_name=item_name).first()

    def __repr__(self):
        return '<menuitem: %r>' % self.item_name


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(32), unique=True)
    cafe_space_position = db.Column(db.String(16), unique=True)
    reserved = db.Column(db.Boolean, default=False)
    receipts = db.relationship('Receipt', backref='table', lazy='dynamic')

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(table_id):
        return Table.query.filter_by(id=table_id).first()

    @staticmethod
    def find_table(id):
        return Table.query.filter_by(id=id).first()

    def __repr__(self):
        return '<table number: %r>' % self.id


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    email = db.Column(db.String(60), unique=True)
    comments = db.Column(db.String(1000))
    is_delete = db.Column(db.Boolean, default=False)

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(comment_id):
        return Table.query.filter_by(id=comment_id).first()

    def __repr__(self):
        return '<comment number: %r>' % self.id


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menuitem.id'))
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt.id'))
    item_count = db.Column(db.SmallInteger)
    status = db.Column(db.String(32), default='waiting')
    submit_time = db.Column(db.DateTime)
    is_delete = db.Column(db.Boolean, default=False)

    @staticmethod
    def find_order_by_id(order_id):
        return Order.query.filter_by(id=order_id).first()

    @staticmethod
    def select_all():
        return db.session.execute('SELECT * FROM public."order" ORDER BY id Desc')

    @staticmethod
    def find_most_popular_items(count):
        return db.session.execute(
            f'SELECT menu_item_id , Count(menu_item_id) FROM public."order" GROUP BY menu_item_id HAVING COUNT(menu_item_id)>1 ORDER BY public."order"."count" DESC limit {count}')

    def create(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<order number: %r>' % self.id


class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    time_stamp = db.Column(db.DateTime)
    pay_status = db.Column(db.Boolean, default=False)
    total_price = db.Column(db.Integer)
    final_price = db.Column(db.Integer)
    orders = db.relationship('Order', backref='receipt', lazy='dynamic')

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def final_receipt(table_id):
        return Receipt.query.filter_by(table_id=table_id).first()

    def __repr__(self):
        return '<receipt: %r>' % self.table_id


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32), unique=True)
    duration = db.Column(db.String(32))
    menu_item = db.relationship('Menuitem', backref='menuitem', lazy='dynamic')

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def find_category(id):
        return Category.query.filter_by(id=id).first()

    def __repr__(self):
        return '<category number: %r>' % self.id
