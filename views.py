from models import *
import os
from database import db
from flask import request, redirect, url_for, make_response, render_template, flash, make_response
from forms import *
import json
from werkzeug.datastructures import ImmutableMultiDict
from datetime import datetime

path = os.path.join("static/img")
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
            menu_items = Menuitem.get_valid_items()
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
        receipt_id = request.cookies.get('Receipt')
        orders = request.form
        orders = orders.to_dict(flat=False)
        for i, j in orders.items():
            orders = i
        orders = json.loads(orders)
        for order in orders:
            menu_item_id = Menuitem.find_item(order["name"]).id
            item_count = order["count"]
            Order(menu_item_id=menu_item_id, receipt_id=receipt_id, item_count=item_count).create()
    elif request.method == "DELETE":
        data_order_id = request.form['data-order-id']
        order = Order.find_order_by_id(data_order_id)
        order.is_delete = True
        order.create()
        return "", 200
    else:
        return "Bad Request !"


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
        menu_items = Menuitem.query.all()
        categories = Category.query.all()
        user_name = Cashier.get_by_id(user_id).username
        menus = {
            "menu_items": menu_items,
            "categories": categories
        }
        receipts = Receipt.query.all()
        total_sales_amount = 0

        for receipt in receipts:
            if not receipt.final_price:
                receipt.final_price = 0
            total_sales_amount += receipt.final_price

        most_pupolar_items = Order.find_most_popular_items()
        most_pupolar_menu_item = []
        for most_item in most_pupolar_items:
            most_pupolar_menu_item.append(Menuitem.get_by_id(most_item[0]))
        print(most_pupolar_menu_item)
        data2 = {
            'menuitem': Menuitem.query.all(),
            'table': Table.query.all(),
            'total_sales_amount': total_sales_amount,
            'order': Order.query.all(),
            "most_popular": most_pupolar_menu_item
        }
        # print(data
        resp = make_response(
            render_template("AdminPanel/dashboard.html", data=data,
                            menu=menus, name=str(user_name), data2=data2))
        return resp
    else:
        base_variables['page']['title'] = 'Login'
        data = base_variables
        return redirect(url_for('login', data=data))


def logout():
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('aetvbhuoaetv')
    return resp


def order_list():
    check_reserve = None
    if request.method == "GET":
        table_id = request.cookies.get("Table")
        if table_id:
            menu_items = Menuitem.query.all()
            receipts = Receipt.query.all()
            orders = Order.query.all()
            return render_template("order_list.html", menu_items=menu_items, orders=orders, table_id=table_id,
                                   receipts=receipts)
        else:
            check_reserve = True
            return redirect(url_for("home", check_reserve=check_reserve, check_msg="Choose Table"))
    elif request.method == "POST":
        table_id = request.cookies.get("Table")
        orders = request.values.get("")
        return f"{table_id} , {orders}"


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
        return render_template('index.html', tables=tables, data=data, msg=msg,
                               check_reserve=check_reserve)
    elif request.method == "POST":
        table_id = request.values.get("table_id")
        if table_id:
            table = Table.get_by_id(table_id)
            table.reserved = True
            table.create()
            flash(f'Congrats! your table id is {table_id}')
            resp = make_response(redirect(url_for("home")))
            create_receipt = Receipt(table_id=table_id, time_stamp=now)
            create_receipt.create()
            resp.set_cookie("Table", f"{table.id}", expires=now + timedelta(hours=3))
            resp.set_cookie("Receipt", f"{create_receipt.id}", expires=now + timedelta(hours=3))
            return resp
        return redirect(url_for('home'))
    else:
        return "bad request"


def menu_item_adder():
    # login requirement
    user_id = request.cookies.get("aetvbhuoaetv")
    if Cashier.get_by_id(user_id):
        if request.method == "GET":
            categories = Category.query.all()
            return render_template("menu_item_adder.html", categories=categories)
        elif request.method == "POST":
            thefile = request.files["file"]
            thefile.filename = request.form["file_name"]
            menu_item_name = request.form["file_name"].split('.')[0]
            price = request.form["price"]
            category_id = request.form["category_id"]
            Menuitem(item_name=menu_item_name, price=price, item_category_id=category_id).create()
            thefile.save(os.path.join(path, thefile.filename))
            return thefile.filename, "Successful uploaded"
        else:
            return "Bad Request"
    else:
        return "Access Denied"


def change_table_status():
    if request.method == "GET":
        return render_template("change_table_status.html")
    elif request.method == "POST":
        now = datetime.now()
        do = request.form["do"]
        table_id = request.form["table_id"]
        table = Table.get_by_id(table_id)
        if bool(int(do)):
            table.reserved = True
            table.create()
            create_receipt = Receipt(table_id=table_id, time_stamp=now)
            create_receipt.create()
        else:
            table.reserved = False
            their_receipt = Receipt.query.filter_by(table_id=table_id, pay_status=False).first()
            their_receipt.pay_status = True
            their_receipt.create()
            # their_orders = Order.query.filter_by(receipt_id=their_receipt.id).all()

        return '', 204

        # table_id = request.form["table_id"].split("-")
        # if table_id[0] == "R":
        #     table = Table.get_by_id(table_id[1])
        #     table.reserved = True
        #     table.create()
        #     return f'{table.table_name} Status Changed'
        # elif table_id[0] == "U":
        #     table = Table.get_by_id(table_id[1])
        #     table.reserved = False
        #     table.create()
        #     return f'{table.table_name} Status Changed'
    else:
        return "Bad Request !"


def show_tables():
    user_id = request.cookies.get("aetvbhuoaetv")
    if Cashier.get_by_id(user_id):
        if request.method == "GET":
            tables = Table.query.order_by(Table.id)
            return render_template('AdminPanel/tables.html', tables=tables)
        elif request.method == "POST":
            return "Coming Soon..."
        else:
            return "Bad Request"
    else:
        return "Access Denied"


def cashier_menu():
    user_id = request.cookies.get("aetvbhuoaetv")
    if Cashier.get_by_id(user_id):
        check_reserve = None
        if request.method == "GET":
            menu_items = Menuitem.query.all()
            categories = Category.query.all()
            return render_template("AdminPanel/cashier_menu.html", menu_items=menu_items, categories=categories)
        elif request.method == "POST":
            item_id = request.form['data-id']
            item = Menuitem.get_by_id(item_id)
            item.is_delete = False
            item.create()
            return "", 200
        elif request.method == "DELETE":
            item_id = request.form['data-id']
            item = Menuitem.get_by_id(item_id)
            item.is_delete = True
            item.create()
            return "", 200
        else:
            return "Bad Request"
    else:
        return "Access Denied"
