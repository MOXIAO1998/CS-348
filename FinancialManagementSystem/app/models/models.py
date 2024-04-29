from app import db, login_manager
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """
    User model
        - id: User ID
        - username: Username
        - password_hash: Password hash
        - email: Email address
        - create_date: Create date
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.username


class BankAccount(db.Model):
    """
    银行账户模型
        - id: 账户ID
        - user_id: 用户ID
        - balance: 余额
        - bank_name: 银行名称
        - create_date: 创建时间
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    bank_name = db.Column(db.String(80), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('bank_accounts', lazy=True))


class PlatformAccount(db.Model):
    """
    platformaccount table
        - id: id for account
        - user_id: user_id foreign id to id in user
        - balance: balance of the aacount
        - create_date: create time
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('platform_accounts', lazy=True))


class Stock(db.Model):
    """
    stock
        - id: stock ID
        - symbol: stock number
        - name: stock name
    """
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)


class UserStock(db.Model):
    """
    UserStock stock user holds
        - id: id for stock hold
        - user_id: user id
        - stock_id: stock id
        - quantity: amount of stock
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref=db.backref('user_stocks', lazy=True))
    stock = db.relationship('Stock', backref=db.backref('stock_users', lazy=True))


class Order(db.Model):
    """
    order
        - id
        - user_id
        - stock_id
        - order_type
        - quantity
        - price
        - status
        - create_date
        - complete_date
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
