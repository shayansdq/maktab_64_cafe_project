from models import *
from database import db
from flask import request, redirect, url_for, make_response, render_template
from forms import *


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


def dashboard():
    user_id = request.cookies.get("aetvbhuoaetv")
    if Cashier.get_by_id(user_id):
        user_name = Cashier.get_by_id(user_id).username
        resp = make_response(render_template("dashboard.html", name=str(user_name)))
        return resp
    else:
        return redirect(url_for('login'))


def logout():
    resp = make_response(redirect(url_for('home')))
    resp.delete_cookie('aetvbhuoaetv')
    return resp


def home():
    return render_template('index.html')