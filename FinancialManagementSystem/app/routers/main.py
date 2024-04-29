from flask import blueprints, render_template, request, redirect, url_for, flash
from app import db
from flask_login import login_required, current_user
from sqlalchemy import text
from app.models import PlatformAccount, UserStock, Order, Stock

bp = blueprints.Blueprint('main', __name__, url_prefix='/main')


@bp.route('/index', endpoint='index')
@login_required
def index():

    query_sql = text(f"""
        SELECT o.id, u.username, s.symbol, o.quantity, o.price
        FROM 'order' o
        JOIN user u ON o.user_id = u.id
        JOIN stock s ON o.stock_id = s.id
        WHERE o.quantity > 0 and o.user_id != {current_user.id};
    """)

    orders = db.session.execute(query_sql).fetchall()

    orders = list(map(lambda x: {
        'id': x.id,
        'stock_symbol': x.symbol,
        'username': x.username,
        'quantity': x.quantity,
        'price': x.price
    }, orders))

    print(orders)

    return render_template('index.html', orders=orders)


@bp.route('/personal', endpoint='personal')
@login_required
def personal():
    user_id = current_user.id

    query_sql = text(f"""
        SELECT s.symbol AS stock_symbol, us.quantity AS quantity
        FROM user_stock us
        JOIN stock s ON us.stock_id = s.id
        WHERE us.user_id={user_id};
    """)

    portfolio_items = db.session.execute(query_sql).fetchall()
    portfolio_items = list(map(lambda x: {
        'stock_symbol': x[0],
        'quantity': x[1]
    }, portfolio_items))

    query_sql = text(f"""
        SELECT balance
        FROM platform_account
        WHERE user_id={user_id};
    """)
    balance = db.session.execute(query_sql).fetchone()
    balance = balance[0] if balance else 0

    return render_template('personal.html', user={
        'username': current_user.username,
        'email': current_user.email,
        'balance': balance
    }, portfolio_items=portfolio_items)


@bp.route('/sell', methods=['GET', 'POST'], endpoint='sell')
@login_required
def cell():
    if request.method == 'POST':
        stock_symbol = request.form.get('stock_symbol')
        quantity = request.form.get('quantity')
        price = request.form.get('price')

        if not stock_symbol or not quantity or not price:
            flash('All fields are required', 'danger')
            return redirect(url_for('main.main.sell'))

        try:
            stock_id = Stock.query.filter_by(symbol=stock_symbol).first().id
            quantity = int(quantity)
            price = float(price)
            if quantity <= 0 or price <= 0:
                raise ValueError('Invalid quantity or price')
            user_id = current_user.id
            user_stock = UserStock.query.filter_by(user_id=user_id, stock_id=stock_id).first()
            if not user_stock or user_stock.quantity < quantity:
                flash('Insufficient quantity', 'danger')
                return redirect(url_for('main.main.sell'))
            order = Order(user_id=user_id, stock_id=stock_id, quantity=quantity, price=price)
            db.session.add(order)
            user_stock.quantity -= quantity
            db.session.commit()
            flash('Sell successfully', 'success')
            return redirect(url_for('main.main.sell'))

        except ValueError:
            flash('Invalid quantity or price', 'danger')
            return redirect(url_for('main.main.sell'))

    else:
        user_id = current_user.id

        query_sql = text(f"""
            SELECT s.symbol AS stock_symbol, us.quantity AS quantity
            FROM user_stock us
            JOIN stock s ON us.stock_id = s.id
            WHERE us.user_id={user_id};
        """)

        portfolio_items = db.session.execute(query_sql).fetchall()
        portfolio_items = list(map(lambda x: {
            'stock_symbol': x[0],
            'quantity': x[1]
        }, portfolio_items))

        query_sql = text(f"""
            SELECT o.id, st.symbol AS stock_symbol, o.quantity, o.price
            FROM 'order' o
            JOIN stock st ON o.stock_id = st.id
            WHERE o.user_id = {user_id};
        """)

        order_items = db.session.execute(query_sql).fetchall()
        order_items = list(map(lambda x: {
            'id': x[0],
            'stock_symbol': x[1],
            'quantity': x[2],
            'price': x[3]
        }, order_items))

        return render_template('sell.html',
                               owned_stocks=portfolio_items,
                               selling_orders=order_items
                               )
