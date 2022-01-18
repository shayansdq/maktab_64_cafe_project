from core.model import *
from flask import request, redirect, url_for, render_template, flash, make_response, abort
from cashier.forms import *
import json
from datetime import datetime
from core.data import *


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

    if False:
        abort(404)


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

    if False:
        abort(404)


def menu():
    if request.method == "GET":
        table_id = request.cookies.get("Table")
        if table_id:
            menu_items = Menuitem.get_valid_items()
            categories = Category.query.all()
            return render_template("menu.html", menu_items=menu_items, categories=categories, status=True)
        else:
            menu_items = Menuitem.get_valid_items()
            categories = Category.query.all()
            return render_template("menu.html", menu_items=menu_items, categories=categories, status=False)
    elif request.method == "POST":
        table_id = request.cookies.get("Table")
        orders = request.values.get("")
        return f"{table_id} , {orders}"

    if False:
        abort(404)


def send_order():
    if request.method == "POST":
        now = datetime.now()
        receipt_id = request.cookies.get('Receipt')
        orders = request.form
        orders = orders.to_dict(flat=False)
        for i, j in orders.items():
            orders = i
        orders = json.loads(orders)
        for order in orders:
            menu_item_id = Menuitem.find_item(order["name"]).id
            item_count = order["count"]
            Order(menu_item_id=menu_item_id, receipt_id=receipt_id,
                  item_count=item_count, submit_time=datetime.now()).create()
        return "", 204
    elif request.method == "DELETE":
        data_order_id = request.form['data-order-id']
        order = Order.find_order_by_id(data_order_id)
        order.is_delete = True
        order.create()
        return "", 200
    else:
        return "Bad Request !"

    if False:
        abort(404)

