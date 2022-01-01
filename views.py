from models import *
from database import db
from flask import request, redirect, url_for, make_response, render_template, flash, make_response
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
    if request.method == "GET":
        tables = Table.query.all()
        return render_template('index.html', tables=tables)
    elif request.method == "POST":
        table_id = request.values.get("table_id")
        if table_id:
            table = Table.get_by_id(table_id)
            table.reserved = True
            table.create()
            resp = make_response(redirect(url_for("home")))
            resp.set_cookie("Table", f"{table.id}")
            return resp
        return "bad request"
    else:
        return "bad request"
