from flask import Flask, render_template, redirect, url_for, Response, make_response, request
from database import db
from flask_bootstrap import Bootstrap
from os import urandom
from landing.views import *
from cashier.views import *
from cashier.spa_views import *


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

app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])

app.add_url_rule('/cashier/dashboard', 'dashboard', dashboard, methods=['GET', 'POST'])

app.add_url_rule('/logout', 'logout', logout)

app.add_url_rule('/', 'home', home, methods=["GET", "POST"])


# app.add_url_rule("/handler/", "handler", spa_handler)


@app.errorhandler(404)
def showerror(error):
    return render_template("page error 404.html"), 404


app.add_url_rule('/show_comments', 'show_comments', show_comments, methods=['GET', 'POST'])


@app.errorhandler(404)
def showerror(error):
    return render_template("page error 404.html"), 404


app.add_url_rule('/menu', 'menu', menu, methods=["GET", "POST"])


@app.errorhandler(404)
def showerror(error):
    return render_template("page error 404.html"), 404


app.add_url_rule('/menu/order_list', 'order_list', order_list, methods=["GET", "POST"])


@app.errorhandler(404)
def showerror(error):
    return render_template("page error 404.html"), 404


app.add_url_rule('/send_order', 'send_order', send_order, methods=["POST", "DELETE"])


@app.errorhandler(404)
def showerror(error):
    return render_template("page error 404.html"), 404


app.add_url_rule('/cashier_order', 'cashier_order', cashier_order, methods=["GET", "POST", "DELETE", "PUT"])


@app.errorhandler(404)
def showerror(error):
    return render_template("page error 404.html"), 404


app.add_url_rule('/cashier/change_table_status', "change_table_status", change_table_status, methods=["GET", 'POST'])


@app.errorhandler(404)
def showerror(error):
    return render_template("page error 404.html"), 404


app.add_url_rule('/cashier/show_tables', "show_tables", show_tables, methods=["GET", 'POST'])


@app.errorhandler(404)
def showerror(error):
    return render_template("page error 404.html"), 404


app.add_url_rule('/cashier/menu', "cashier_menu", cashier_menu, methods=["GET", 'POST', "DELETE"])


@app.errorhandler(404)
def showerror(error):
    return render_template("page error 404.html"), 404


app.add_url_rule('/cashier/menu/menu_item_adder', 'menu_item_adder', menu_item_adder, methods=["GET", "POST"])


@app.errorhandler(404)
def showerror(error):
    return render_template("page error 404.html"), 404


app.add_url_rule('/cashier/menu/receipts', 'receipts', receipts_data, methods=["GET", "POST"])


@app.errorhandler(404)
def showerror(error):
    return render_template("page error 404.html"), 404


app.add_url_rule('/orderbyrid', 'order_bt_receipts_id', order_of_receipt, methods=["POST"])

@app.errorhandler(404)
def showerror(error):
    return render_template("page error 404.html"), 404


if __name__ == '__main__':
    app.run()



# git test