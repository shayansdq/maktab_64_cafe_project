from flask import Flask, render_template, redirect, url_for, Response, make_response, request
from database import db
from flask_bootstrap import Bootstrap
from os import urandom
from views import *


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

app.add_url_rule('/dashboard', 'dashboard', dashboard, )

app.add_url_rule('/logout', 'logout', logout)

app.add_url_rule('/', 'home', home, methods=["GET", "POST"])

app.add_url_rule('/menu', 'menu', menu, methods=["GET", "POST"])

app.add_url_rule('/send_order', 'send_order', send_order, methods=["POST"])

app.add_url_rule('/upload', 'upload', uploader, methods=["GET", "POST"])

if __name__ == '__main__':
    app.run()
