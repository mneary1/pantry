import os, sqlite3, math, requests
from flask import Flask, url_for, render_template, request, redirect, session, abort, flash, g
from flask.ext import login
from flask.ext.login import LoginManager, login_user, logout_user, current_user
from flask.ext.security import login_required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import *
from pygeocoder import Geocoder
from pagination import Pagination

app = Flask(__name__)
app.config.from_object(__name__)

# App settings
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'pantry.db'),
    DEBUG=True,
    SECRET_KEY='pantry key',
))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE']

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

PER_PAGE = 10

venmo_api_code = ''

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
    geo_x = db.Column(db.Float)
    geo_y = db.Column(db.Float)
    created_at = db.Column(db.TIMESTAMP)

    def __init__(self, username, password, real_name, address, email):
        self.username = username
        self.password = password
        self.real_name = real_name
        self.address = address
        self.email = email

        geo_results = Geocoder.geocode(self.address)
        self.geo_x = geo_results[0].coordinates[0]
        self.geo_y = geo_results[0].coordinates[1]

    def check_password(self, other_pass):
        return self.password == other_pass

    def is_authenticated(self):
        return session['user_id'] == self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.username

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

class LoginForm(Form):
    username = TextField(validators=[required()])
    password = PasswordField(validators=[required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        # rv = Form.validate(self)
        # if not rv:
        #     return False

        user = User.query.filter_by(username=self.username.data).first()

        if user is None:
            #self.username.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            #self.username.errors.append('Invalid password')
            return False

        self.user = user
        return True

    def get_user(self):
        return db.session.query(User).filter_by(username=self.username.data).first()

@app.route("/")
def pantry():
    print request.path
    return render_template('home.html')

@app.route("/add_to_pantry", methods=["POST"])
def add_to_pantry():
    foods = request.form['food-names-pantry']
    if(foods):
        foods = foods.replace(' ', '').rstrip(',')
        if current_user.items_available:
            current_user.items_available += ',' + foods
        else:
            current_user.items_available = foods
        db.session.commit()
        flash("Added new foods to your pantry!", 'success')
    else:
        flash("Invalid food list supplied. Sorry.", 'error')
    return redirect(url_for('dashboard'))

@app.route("/add_to_sl", methods=["POST"])
def add_to_sl():
    foods = request.form['food-names-sl']
    if(foods):
        foods = foods.replace(' ', '').rstrip(',')
        if current_user.items_desired:
            current_user.items_desired += ',' + foods
        else:
            current_user.items_desired = foods
        db.session.commit()
        flash("Added new foods to your shopping list!", 'success')
    else:
        flash("Invalid food list supplied. Sorry.", 'error')
    return redirect(url_for('dashboard'))

@app.route("/dashboard", defaults={'page':1})
@app.route("/dashboard/<int:page>")
@login_required
def dashboard(users=[], user_pantry=[], user_sl=[], geo_info=[], page=1):
    if current_user.items_available:
        user_pantry = current_user.items_available.split(',')

    if current_user.items_desired:
        user_sl = current_user.items_desired.split(',')

    cx, cy = current_user.geo_x, current_user.geo_y
    users = User.query.order_by('abs(geo_x - {}) + abs(geo_y - {})'.format(cx, cy))

    names = [user.real_name for user in users]
    dists = [round(haversine_miles(user.geo_x, user.geo_y, cx, cy), 2) for user in users]
    geo_info = {name:dist for (name, dist) in zip(names, dists)}

    count = users.count()
    users = users.offset(PER_PAGE * (page - 1)).limit(PER_PAGE)
    pagination = Pagination(page, PER_PAGE, count)
    return render_template('dashboard.html', users=users, \
            user_pantry=user_pantry, user_sl=user_sl, geo_info = geo_info, pagination=pagination)


@app.route("/empty_pantry")
def empty_pantry():
    current_user.items_available = ''
    db.session.commit()
    flash("Cleared your list!", 'success')
    return redirect(url_for('dashboard'))

@app.route("/empty_sl")
def empty_sl():
    current_user.items_desired = ''
    db.session.commit()
    flash("Cleared your list!", 'success')
    return redirect(url_for('dashboard'))

@app.route("/find/<food>")
def find(users=[], food=None, geo_info=[]):
    if food:
        cx, cy = current_user.geo_x, current_user.geo_y
        users = User.query.order_by('abs(geo_x - {}) + abs(geo_y - {})'.format(cx, cy)) \
                          .filter(User.items_available.contains(food)).all()
        names = [user.real_name for user in users]
        dists = [round(haversine_miles(user.geo_x, user.geo_y, cx, cy), 2) for user in users]
        geo_info = {name:dist for (name, dist) in zip(names, dists)}

    return render_template('find.html', users=users, food=food, geo_info=geo_info)

@app.route("/examples")
def examples():
    return render_template('examples.html')

@app.route("/login", methods=["GET", "POST"])
def login(form=None):
    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user()
        login_user(user)
        flash("Logged in!", 'success')
        session['user_id'] = form.user.id
        g.user = user
        return redirect(request.args.get("next") or url_for('dashboard'))
    if(form.username.data):
        flash("Bad login credentials, try again!", 'error')
    return render_template("home.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out!", 'success')
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if(request.method == 'GET'):
        return render_template('register.html')
    else:
        username = request.form['username']
        password = request.form['password']
        realname = request.form['realname']
        address = request.form['address']
        email = request.form['email']

        data = [username, password, realname, address, email]
        if any(not field for field in data):
            flash("Everything is required! Everything! Do it over!", 'error')
            return render_template('register.html')

        new_guy = User(*data)
        db.session.add(new_guy)
        db.session.commit()

        flash("That's pretty much it. You're registered. Have fun!", 'success')
        return render_template('home.html')

@app.route('/venmo')
def venmo_login():
    return redirect('https://api.venmo.com/v1/oauth/authorize?client_id=2284&response_type=code&scope=make_payments')

@app.route('/venmo2')
def venmo_connect():
    try:
        venmo_api_code = request.args.get('code')
    except:
        flash("Venmo API Connect failed.")
        return redirect('/')

    data = {}
    data ['client_id'] = '2284'
    data ['client_secret'] = '4L23sdF428pwBQYrMe3UQKrdQpdC4GvC'
    data ['code'] = venmo_api_code
    data ['scope'] = 'make_payments'

    url = 'https://api.venmo.com/v1/oauth/access_token'

    response = requests.post(url,data)

    print response.json()

    return redirect('/')

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

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

# Calculates the distance (in miles) between two geo coordinates.
# http://stackoverflow.com/questions/365826/calculate-distance-between-2-gps-coordinates
def haversine_miles(lat1, lon1, lat2, lon2):
    R = 3956;
    dLat = to_rad(lat2-lat1)
    dLon = to_rad(lon2-lon1)
    lat1 = to_rad(lat1)
    lat2 = to_rad(lat2)

    a = math.sin(dLat/2) * math.sin(dLat/2) + \
            math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2);
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a));
    d = R * c;
    return d

def to_rad(deg):
    return (math.pi / 180) * deg

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

if __name__ == "__main__":
    app.run()
