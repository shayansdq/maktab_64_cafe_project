from flask import Flask, render_template, redirect, url_for, Response, make_response, request
from database import db
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from os import urandom
from models import *

def create_app():
    app = Flask(__name__)
    app.secret_key = urandom(24)
    app.config.from_pyfile('config.cfg')
    bootstrap = Bootstrap(app)
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    return app


app = create_app()


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
    user_id = request.cookies.get("aetvbhuoaetv")
    if Cashier.get_by_id(user_id):
        user_name = Cashier.get_by_id(user_id).username
        resp = make_response(render_template("dashboard.html", name=str(user_name)))
        return resp
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('home')))
    resp.delete_cookie('aetvbhuoaetv')
    return resp


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
