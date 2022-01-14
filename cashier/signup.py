from maktab_64_cafe_project.database import db
from maktab_64_cafe_project.cashier.model import Cashier
import psycopg2
import psycopg2.extras
from psycopg2._psycopg import connection, cursor
import argparse
from werkzeug.security import generate_password_hash, check_password_hash

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--first_name", required=True)
    parser.add_argument("-l", '--last_name', required=True)
    parser.add_argument("-u", '--username', required=True)
    parser.add_argument("-n", '--phone_number', required=True)
    parser.add_argument("-e", '--email', required=True)
    parser.add_argument("-p", '--password_hash', required=True)
    args = parser.parse_args()

    print('step1')
    first_name = args.first_name
    last_name = args.last_name
    username = args.username
    phone_number = args.phone_number
    email = args.email
    password_hash = generate_password_hash(args.password_hash, method='sha256')
    conn: connection = psycopg2.connect(dbname="gkfiljss", user='gkfiljss', host='kashin.db.elephantsql.com', port=5432, password="AftCRK0OqR14N6XffDFBimNvv3-aONHt")
    curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    curs.execute(
        f"""INSERT INTO cashier (first_name,last_name,username,phone_number,email,password_hash) VALUES (%s,%s,%s,%s,%s,%s)""",
        (first_name, last_name, username, phone_number, email, password_hash))
    conn.commit()
    # user = Cashier(first_name=first_name, last_name=last_name, username=username, phone_number=phone_number,
    #                email=email, password_hash=password_hash)
    # user.create()
# url_for('static',file_name='img/asd.jpg')