import os, sqlite3
from flask import Flask, url_for, render_template, request, redirect, session, abort, flash, g
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(__name__)

# App settings
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'pantry.db'),
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./pantry.db',
    DEBUG=True,
    SECRET_KEY='pantry key',
))

db = SQLAlchemy(app)

# login_manager = LoginManager()
# login_manager.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    real_name = db.Column(db.String(80), unique=True)
    address = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    items_available = db.Column(db.String(1000))
    items_desired = db.Column(db.String(1000))
    points = db.Column(db.Integer)
    num_given = db.Column(db.Integer)
    num_bought = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP)

    def __init__(self, username, password, real_name, address, email):
        self.username = username
        self.password = password
        self.real_name = real_name
        self.address = address
        self.email = email

    def __repr__(self):
        return '<User {} {} {} {}' \
                .format(self.username, self.real_name, self.address, self.email)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_from = db.Column(db.String(80))
    name_to = db.Column(db.String(80))
    item = db.Column(db.String(80))
    price = db.Column(db.Float)
    created_at = db.Column(db.TIMESTAMP)

    def __init__(self, name_from, name_to, item, price):
        self.name_from = name_from
        self.name_to = name_to
        self.item = item
        self.price = price

    def __repr__(self):
        return 'Transaction {} {} {} {}' \
               .format(self.name_from, self.name_to, self.item, self.price)

@app.route("/")
def pantry():
    return render_template('home.html')

@app.route("/examples")
def examples():
    return render_template('examples.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# @login_manager.user_loader
# def load_user(userid):
#     return User.get(userid)

if __name__ == "__main__":
    app.run()
