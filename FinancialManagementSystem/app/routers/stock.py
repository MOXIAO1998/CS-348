from flask import blueprints, request
from flask import jsonify
from app import db
from flask_login import login_required, current_user
from app.models import PlatformAccount, UserStock, Order
from sqlalchemy.exc import SQLAlchemyError

bp = blueprints.Blueprint('stock', __name__, url_prefix='/cancel')


@bp.route('/cancel_order', methods=['POST'], endpoint='cancel_order')
@login_required
def cancel_order():
    data = request.get_json()
    order_id = data.get('order_id')

    try:
        order = Order.query.with_for_update().filter_by(id=order_id).first()
        if not order:
            return jsonify({'status': 'error', 'message': "Order doesn't exist"}), 404

        if order.user_id != current_user.id:
            return jsonify({'status': 'error', 'message': 'No permission'}), 403

        user_stock = UserStock.query.filter_by(user_id=current_user.id, stock_id=order.stock_id).first()
        if user_stock:
            user_stock.quantity += order.quantity
        else:
            user_stock = UserStock(user_id=current_user.id, stock_id=order.stock_id, quantity=order.quantity)
            db.session.add(user_stock)

        db.session.delete(order)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Order is already canceled'})

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'An error occurred during the buying process'}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'An error occurred during order cancellation'}), 500


@bp.route('/buy', methods=['POST'], endpoint='buy')
@login_required
def buy():
    data = request.get_json()
    order_id = data.get('order_id')
    quantity = float(data.get('quantity'))

    try:
        order = Order.query.filter_by(id=order_id).first()
        if not order:
            return jsonify({'status': 'error', 'message': "Order doesn't exist"}), 404

        if order.user_id == current_user.id:
            return jsonify({'status': 'error', 'message': "Can't buy your own order"}), 403

        if order.quantity < quantity:
            return jsonify({'status': 'error', 'message': "Quantity is not enough"}), 403

        buyer_account = PlatformAccount.query.filter_by(user_id=current_user.id).first()
        seller_account = PlatformAccount.query.filter_by(user_id=order.user_id).first()

        if buyer_account.balance < order.price * quantity:
            return jsonify({'status': 'error', 'message': "Balance is not enough"}), 403

        buyer_account.balance -= order.price * quantity
        seller_account.balance += order.price * quantity

        user_stock = UserStock.query.filter_by(user_id=current_user.id, stock_id=order.stock_id).first()
        if user_stock:
            user_stock.quantity += quantity
        else:
            user_stock = UserStock(user_id=current_user.id, stock_id=order.stock_id, quantity=quantity)
            db.session.add(user_stock)

        order.quantity -= quantity
        if order.quantity == 0:
            db.session.delete(order)

        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Buy successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'An error occurred during the buying process'}), 500
