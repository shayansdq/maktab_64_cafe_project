from views import *


app.add_url_rule("/", "login_page", login_page, methods=["GET", "POST"])
app.add_url_rule("/register", "register_page", register_page, methods=["GET", "POST"])

if __name__ == '__main__':
    app.run()
