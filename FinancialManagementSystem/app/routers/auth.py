from flask import blueprints, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user
from app.models import User
from app import db
from werkzeug.security import check_password_hash

bp = blueprints.Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # if the user is already authenticated, redirect to the index page
    if current_user.is_authenticated:
        return redirect(url_for('main.main.index'))  # 确保使用正确的端点名

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            # Login the user
            login_user(user)
            flash('You have been successfully logged in.', 'success')

            # Redirect to the next page
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.main.index'))  #
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'], endpoint='register')
def register():
    if request.method == 'POST':
        # Get the form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the user already exists
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first() is not None

        # If user exists, redirect to register page
        if user_exists:
            flash('Username or Email already exists.', 'danger')
            return redirect(url_for('main.auth.register'))

        # Create a new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created successfully!', 'success')
        return redirect(url_for('main.auth.login'))

    return render_template('register.html')


@bp.route('/logout', endpoint='logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.auth.login'))  # 确保这里的端点名称与你的登录视图匹配
