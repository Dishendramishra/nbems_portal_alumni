# ========================================
#       standard files/ libraries
# ========================================
# import php2python_encry
# from form import LoginForm, PasswordChangeForm
from flask import *
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
# from flask_mysqldb import MySQL
# from flask_qrcode import QRcode
from flask_mongoengine import MongoEngine
import pymongo
# import pandas as pd
from inspect import cleandoc as I

from datetime import datetime
from pprint import pprint
import os
import hashlib
# ========================================


# ==================================================================
#                    Flask app config
# ==================================================================
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "data"
app.secret_key = "215e04a16e8ed302c48e4474a6fd052702e0f5cc5c85b044b0308c7a038e8dc6"

CORS(app, expose_headers=["Content-Disposition"])

# ==================================================================
#                           MongoDB Setup
# ==================================================================
app.config['MONGODB_SETTINGS'] = {
    'db'  : "alumni",
    'host': "localhost",
    'port': 27017,
    'username' : "admin",
    'password' : "nothing",
    'authentication_source': 'admin'
}
db = MongoEngine(app)
myclient = pymongo.MongoClient(
    "mongodb://127.0.0.1:27017/", 
    username = "admin",
    password = "nothing"
)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'
login_manager.login_message = u"Please log in to access this page."
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


mydb = myclient["alumni"]
mycoll = mydb["users"]


class User(UserMixin):
    def __init__(self, username, password, email):
        self.username = username 
        self.password = password
        self.email = email

    @staticmethod
    def get(user_id):
        
        result = list(mycoll.find({"email":user_id}))

        if result:
            return User(result[0]["username"], result[0]["password"], result[0]["email"])
        else:
            return False

    def get_id(self):
           return (self.email)

    def is_authenticated(self):
        return True
# ==================================================================



# ==================================================================
#                    MongoDB Setup for Login Manager
# ==================================================================
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'
login_manager.login_message = u"Please log in to access this page."
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
# ==================================================================


@app.route('/favicon')
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET', "POST"])
@app.route('/login', methods=['GET', "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    elif request.method == "GET":
        return render_template("login.html")

    # request.method is POST
    else:
        email = request.form["email"]
        password = request.form["password"]
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        # password_hash = php2python_encry.encryption(password, "e")


        # cursor = mysql.connection.cursor()
        # query = f"SELECT pan, name, email, mobile from user where password = '{password_hash}' && email = '{email}';"
        # cursor.execute("USE nbeedu_sulekha;")
        # cursor.execute(query)
        # result = cursor.fetchone()

        # cursor.execute("USE nbeedu_empprofiledb;")
        # cursor.execute(
        #     f"SELECT emp_photo from emplogbook_tbl where emp_email='{email}';")
        # photo = cursor.fetchone()
        # cursor.close()

        result = list(mycoll.find({"email":email, "password": password_hash}))
        print(result)
        print(email, password_hash)

        if result:
            user = User(result[0]["username"], result[0]["password"], result[0]["email"])
            login_user(user)

            return redirect(url_for("home"))

        else:
            return "Bad Credientials!"


@app.route('/home', methods=['GET', "POST"])
@login_required
def home():
    return render_template("home.html")

@app.route('/userinfo', methods=['GET', "POST"])
@login_required
def userinfo():
    return render_template("userinfo.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True