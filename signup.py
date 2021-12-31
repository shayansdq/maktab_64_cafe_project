from database import db
import argparse
from werkzeug.security import generate_password_hash, check_password_hash
from abc import ABC
import psycopg2
import psycopg2.extras
from psycopg2._psycopg import connection, cursor
from app import Cashier

# def create(args):
#     conn: connection = psycopg2.connect(dbname="flash_cards", user="mohammadreza", host="localhost", port=5432, password=7985)
#     with conn:
#         curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#         print('connection created')
#         with curs:
#             curs.execute(
#                 f"""INSERT INTO users(username, password) VALUES (%s, %s);""", (args.username, args.password)
#                )
#             return "ok"


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

    def create(self):
        db.session.add(self)
        db.session.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", required=True)
    parser.add_argument("-p", '--password', required=True)
    args = parser.parse_args()

    print('step1')
    username = args.username
    password = args.password

    user.create()
