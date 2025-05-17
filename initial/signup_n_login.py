from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# User model
class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password = password

    def get_id(self):
        return self.id

# User database (replace this with your own database implementation)
users = {
    'user1': User('user1', 'password1'),
    'user2': User('user2', 'password2')
}

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Routes
@app.route('/')
def index():
    return 'Welcome to the homepage!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return 'Welcome to the dashboard!'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return 'Username already exists'
        user = User(username, password)
        users[username] = user
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
