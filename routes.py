from flask import render_template, redirect, url_for, request
from app import app, db, login_manager
from models import User
from flask_login import login_user, login_required, logout_user, current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            login_user(user)
            return redirect(url_for('dashboard'))

    return render_template('login.html')

import subprocess

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    output = None

    if request.method == 'POST':
        user_input = request.form.get('word')

        try:
            result = subprocess.run("echo " + user_input, shell=True, capture_output=True, text=True)
            output = result.stdout.strip()
        except Exception as e:
            output = str(e)

    return render_template('dashboard.html', name=current_user.username, output=output)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# ✅ NEW: Register route (creates users in DB)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "User already exists"

        # Create new user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


