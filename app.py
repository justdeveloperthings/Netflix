from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask import flash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:@localhost/Netflix"
app.secret_key = 'newtryout'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email = db.Column(db.String(255), nullable=False)
    Password = db.Column(db.String(255), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# REGISTERATION
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(Email=email).first()
        if user:
            flash("Email already exists.")
            return render_template('signup.html')
        else:
            entry = Users(Email=email, Password=password)
            db.session.add(entry)
            db.session.commit()
        return redirect('/login')
    return render_template('signup.html')

# LOGIN
@app.route("/", methods=['GET', 'POST'])
def mainpage():
    if current_user.is_authenticated:
        return render_template('home.html')
    if request.method == 'POST':
        email = request.form.get('email')
        user = Users.query.filter_by(Email=email).first()
        if user:
            return redirect('/login')
        else:
            return redirect('/signup')

    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(Email=email).first()
        if user and password == user.Password:
            login_user(user, remember=True)
            return render_template('home.html')
        else:
            flash('Please check your Email and Password and try again!!')
            return render_template('login.html')
    return render_template('login.html')




# HOME
@app.route("/home")
@login_required
def home():
    return render_template('home.html')

# Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
