from models import *
import os
from database import db
from flask import request, redirect, url_for, make_response, render_template, flash, make_response
from forms import *
import json
from werkzeug.datastructures import ImmutableMultiDict

path = os.path.join("uploads")
os.makedirs(path, exist_ok=True)

base_variables = {
    "page": {
        "base_title": "Cafe Dark",
        "lang": 'en-US',
        "title": 'main'
    },
    'reserve-button': {
        'content': 'Reservation'
    }
}


def menu():
    check_reserve = None
    if request.method == "GET":
        table_id = request.cookies.get("Table")
        if table_id:
            menu_items = Menuitem.query.all()
            categories = Category.query.all()
            return render_template("menu.html", menu_items=menu_items, categories=categories)
        else:
            check_reserve = True
            return redirect(url_for("home", check_reserve=check_reserve, check_msg="Choose Table"))
    elif request.method == "POST":
        table_id = request.cookies.get("Table")
        orders = request.values.get("")
        return f"{table_id} , {orders}"


def send_order():
    if request.method == "POST":
        # todo : must be get receipt id
        table_id = request.cookies.get('Table')
        orders = request.form
        orders = orders.to_dict(flat=False)
        for i, j in orders.items():
            orders = i
        orders = json.loads(orders)
        for order in orders:
            menu_item_id = Menuitem.find_item(order["name"]).id
            item_count = order["count"]
            # todo : create part of get receipt id in menu part
            Order(menu_item_id=menu_item_id, receipt_id=table_id, item_count=item_count).create()
    return '', 204


def login():
    base_variables['page']['title'] = 'Cashier Login'
    data = base_variables
    form = LoginForm()
    if request.cookies.get("aetvbhuoaetv"):
        return redirect(url_for('dashboard', data=data))
    elif form.validate_on_submit():
        user = Cashier.check_user(form.username.data)
        if user:
            if user.verify_password(form.password.data):
                base_variables['page']['title'] = 'Dashboard'
                resp = make_response(redirect(url_for('dashboard', data=data)))
                resp.set_cookie("aetvbhuoaetv", str(user.id))
                return resp
        return '<h1 style="color:red">Invalid Username/Password</h1>'
    return render_template('login-page.html', data=data, form=form)


def dashboard():
    user_id = request.cookies.get("aetvbhuoaetv")
    if Cashier.get_by_id(user_id):
        base_variables['page']['title'] = 'Dashboard'
        data = base_variables
        user_name = Cashier.get_by_id(user_id).username
        resp = make_response(render_template("dashboard.html", data=data, name=str(user_name)))
        return resp
    else:
        base_variables['page']['title'] = 'Login'
        data = base_variables
        return redirect(url_for('login', data=data))


def logout():
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('aetvbhuoaetv')
    return resp


def home():
    from datetime import datetime, timedelta
    now = datetime.now()
    check_reserve = False
    if request.method == "GET":
        base_variables['page']['title'] = 'Home'
        data = base_variables
        table_id = request.cookies.get('Table')
        if request.args.get("check_reserve"):
            msg = request.args.get("check_msg")
            check_reserve = request.args.get("check_reserve")
        else:
            msg = f'Congrats! your table number is: {table_id}'
        tables = Table.query.all()
        if table_id:
            data['reserve-button']['content'] = f'Your table id : {table_id}'
            data['chose-table'] = [f'{table_id}']
        return render_template('index.html', tables=tables, data=data, msg=msg, check_reserve=check_reserve)
    elif request.method == "POST":
        table_id = request.values.get("table_id")
        if table_id:
            table = Table.get_by_id(table_id)
            table.reserved = True
            table.create()
            flash(f'Congrats! your table id is {table_id}')
            resp = make_response(redirect(url_for("home")))
            # todo : must be change this part
            resp.set_cookie("Table", f"{table.id}", expires=now + timedelta(hours=3))
            return resp
        return redirect(url_for('home'))
    else:
        return "bad request"


def uploader():
    return render_template("upload.html")

def save_file():
    thefile = request.files["file"]
    thefile.save(os.path.join(path, thefile.filename))
    return thefile.filename, "Successful upload"