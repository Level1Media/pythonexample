import os
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from flask_caching import Cache
import bcrypt



# gets flasks and stets static directory
app = Flask(__name__, static_folder = "static")
app.config['STATIC_FOLDER'] = 'static'

cache = Cache(config={'CACHE_TYPE': 'simple'})

cache.init_app(app)





app.config['MONGO_DBNAME'] = 'loginexample'
app.config['MONGO_URI'] = 'mongodb://Eli:janemba@ds027165.mlab.com:27165/loginexample'

mongo = PyMongo(app)

@app.route('/')

def index():

    return render_template('index.html', title='Home')

@app.errorhandler(404)
def page_not_found(e):
	return ("404")


@app.route('/dashboard')

def dashboard():
    return render_template("dashboard.html", title='Dashboard', name=session['username'])






@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('dashboard'))

    return 'Invalid username/password combination'






@app.route('/register', methods=['POST', 'GET'])

def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('dashboard'))
        
        return 'That username already exists!'

    return render_template('register.html')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)