from flask import render_template, request
from core.data import base_variables
from core.model import *


# def spa_handler():
    # if request.args.get('show_tables'):
    #     print('hi')
    #     tables = Table.query.order_by(Table.id)
    #     return render_template('cashier-spa/tables.html', tables=tables)
    # elif request.args.get('cashier_order'):
    #     orders = Order.select_all()
    #     menu_items = Menuitem.query.all()
    #     return render_template("cashier-spa/cashier_order.html", orders=orders, menu_items=menu_items)
    # else:
    #     data = base_variables
    #     data['page']['title'] = "خانه"
    #     return render_template('spa/index.html', data=data)
