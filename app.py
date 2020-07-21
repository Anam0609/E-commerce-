# importing flask features
from flask import Flask, render_template
# uses the flask intergrated form
from flask_wtf import FlaskForm
# from wtform we need to import form fields
from wtforms import StringField, PasswordField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


# classes for the login form
class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')


# classes for the login form



# my app routes to my templates
@app.route('/')
# function to render the html template
def dashboard():
    return render_template('dashboard.html')

# my app routes to my templates
@app.route('/login', methods=['GET', 'POST'])
# function to render the html template
def login():
    # calling the class for the login form
    form = LoginForm()
    if form.validate_on_submit():
       return
    return render_template('login.html', form=form)

# my app routes to my templates
@app.route('/register')
# function to render the html template
def register():
    return render_template('register.html')
# my app routes to my templates
@app.route('/index')
# function to render the html template
def index():
    return render_template('index.html')


# runs the flask app
if __name__ == '__main__':
    app.run(debug=True)