from flask import Flask, render_template, redirect, url_for, Response, make_response, request
from database import db
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from os import urandom

app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(24)
app.config.from_pyfile('config.cfg')
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Cashier.check_user(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.cookies.get("aetvbhuoaetv"):
        return redirect(url_for('dashboard'))
    elif form.validate_on_submit():
        user = Cashier.check_user(form.username.data)
        if user:
            if user.verify_password(form.password.data):
                resp = make_response(redirect(url_for('dashboard')))
                resp.set_cookie("aetvbhuoaetv", str(user.id))
                return resp
        return '<h1>Invalid username or password</h1>'
    return render_template('login-page.html', form=form)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', name='shayan20')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# def create_app():
#     app = Flask(__name__)
#     app.secret_key = urandom(24)
#     app.config.from_pyfile('config.cfg')
#     db.init_app(app)
#     with app.test_request_context():
#         db.create_all()
#     return app


class Cashier(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    username = db.Column(db.String(15), unique=True)
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

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Cashier: %r>' % self.username


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

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def find_item(item_name):
        return Menuitem.query.filter_by(item_name=item_name).first()

    def __repr__(self):
        return '<menuitem: %r>' % self.word


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(32), unique=True)
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
    item_count = db.Column(db.SmallInteger)
    status = db.Column(db.String(32), default='waiting')
    submit_time = db.Column(db.DateTime)
    is_delete = db.Column(db.Boolean, default=False)

    @staticmethod
    def find_orders(table_id):
        return Table.query.filter_by(id=table_id).all()

    def create(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<order number: %r>' % self.id


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


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
