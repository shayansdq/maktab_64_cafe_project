from flask import Flask, render_template
from database import db
from os import urandom


def create_app():
    app = Flask(__name__)
    app.secret_key = urandom(24)
    app.config.from_pyfile('config.cfg')
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    return app


app = create_app()


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
