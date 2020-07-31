# importing flask features
from flask import Flask, render_template, redirect, url_for
#importing bootstrap for wtf forms
from flask_bootstrap import Bootstrap
# uses the flask intergrated form
from flask_wtf import FlaskForm
# from wtform we need to import form fields
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length
# for creating the database with sqlite3
from flask_sqlalchemy import SQLAlchemy
# for secured routes and encrypted passwords
from werkzeug.security import generate_password_hash, check_password_hash
# a user has to login in order to purchase products
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin

# initialising my app
app = Flask(__name__)
# secret key is required for my forms 
app.config['SECRET_KEY'] = 'mysecretkey'
#initialising my database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MyDatabase.db'
db = SQLAlchemy(app)
# importng bootstrap to my app
Bootstrap(app)
#manages the protected routes, makes sure only authenticated users have access to the full page
login_manager = LoginManager()
login_manager.init_app(app)  #initialises login_manager app to the app
login_manager.login_view = 'login'

# database table for my users
class MyUsers(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(15), unique=True)
  fullname = db.Column(db.String(20), nullable=False)
  email = db.Column(db.String(30), nullable=False, unique=True)
  password = db.Column(db.String(20), nullable=False)
 

# database table for customer orders
class CustomerOrder(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  fullname = db.Column(db.String(20), nullable=False)
  email = db.Column(db.String(30), nullable=False)
  address = db.Column(db.String(20), nullable=False)
  province = db.Column(db.String(20), nullable=False)
  city = db.Column(db.String(20), nullable=False)
  zipcode = db.Column(db.String(8), nullable=False)

#helps to identify the user who logged in
@login_manager.user_loader
def load_user(id):
    return MyUsers.query.get(int(id))

# classes for the login form
class LoginForm(FlaskForm):
    # making sure that the fields are filled by the user and have the correct length
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])


# classes for the register form
class RegisteForm(FlaskForm):
    #making sure that the fields are filled by the user and have the correct length
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    fullname = StringField('FullName', validators=[InputRequired(), Length(min=10, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email"),Length(max=30)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])

 # the checkout form
class CustomerForm(FlaskForm):
    fullname = StringField('FullName', validators=[InputRequired(), Length(max=20)])
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email"),Length(max=30)])
    address = StringField('Address', validators=[InputRequired(), Length(max=20)])
    province = StringField('Province', validators=[InputRequired(), Length(max=20)])
    city = StringField('City', validators=[InputRequired(), Length(max=20)])
    zipcode = StringField('Zipcode', validators=[InputRequired(), Length(max=20)])
    
 # app routes for my webpages

@app.route('/')
# function to render the html template
def dashboard():
    return render_template('dashboard.html')

@app.route('/index')
# a user is required to login(protected route)
@login_required
# function to render the html template
def index():
    return render_template('index.html', name=current_user.username)


# my app routes to my templates
@app.route('/register', methods=['GET', 'POST'])
# function to render the html template
def register():
    form = RegisteForm()
    # checks if the form is submitted or not
    if form.validate_on_submit():
       # security feature for hashing passwords
       hashed_password = generate_password_hash(form.password.data, method='sha256')

       User = MyUsers(username=form.username.data, fullname=form.fullname.data, email=form.email.data, password=hashed_password)
       # adds new user to the database
       db.session.add(User)

       # saves/ commits new user to the database
       db.session.commit()

       # after signing up, you are immediately redirected to the login screen
       return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
# function to render the html template
def login():
    # Initializing the login form
    form = LoginForm()
    
    # checks if the form is submitted or not
    if form.validate_on_submit():
        #check if user is in the database
        user = MyUsers.query.filter_by(username=form.username.data).first()

        #if the user credentials match with the ones in the database, user will be logged in to the home page
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))

        #error msg if credentials are invalid
        return "Credentials don't match!"
    return render_template('login.html', form=form)

# logout app route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dashboard'))


@app.route('/products')
# a user is required to login(protected route)
@login_required
# function to render the html template
def products():
    return render_template('products.html', name=current_user.username)


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
# function to render the html template
def checkout():
    form = CustomerForm()
    # checks if the form is submitted or not
    if form.validate_on_submit():
      
       userOrder = CustomerOrder(fullname=form.fullname.data, email=form.email.data, address=form.address.data,
       province=form.province.data, city=form.city.data, zipcode=form.zipcode.data)
       # adds new user to the database
       db.session.add(userOrder)

       # saves/ commits new user to the database
       db.session.commit()

       # after signing up, you are immediately redirected to the login screen
       return redirect(url_for('index'))
    return render_template('checkout.html', form=form, name=current_user.username)

@app.route('/contact')
# function to render the html template
def contact():
    return render_template('contact.html', name=current_user.username)

@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html', name=current_user.username )

@app.route('/about')
def about():
    return render_template('about.html', name=current_user.username)



# runs the flask app
if __name__ == '__main__':
    app.run(debug=True)