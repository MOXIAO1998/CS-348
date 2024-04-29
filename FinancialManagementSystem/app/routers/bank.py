from flask import blueprints, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import BankAccount, PlatformAccount
from app import db

bp = blueprints.Blueprint('bank', __name__, url_prefix='/bank')


@bp.route('/withdraw', methods=['POST'], endpoint='withdraw')
@login_required
def withdraw():
    amount = request.form.get('amount')
    if not amount:
        flash('Amount is required', 'danger')
        return redirect(url_for('main.main.personal'))

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError('Amount must be greater than 0')

        platform_account = PlatformAccount.query.filter_by(user_id=str(current_user.id)).first()
        bank_account = BankAccount.query.filter_by(user_id=str(current_user.id)).first()

        if platform_account.balance < amount:
            flash('Insufficient balance', 'danger')
            return redirect(url_for('main.main.personal'))

        platform_account.balance -= amount
        bank_account.balance += amount
        db.session.commit()

        flash('Withdraw successfully', 'success')
        return redirect(url_for('main.main.personal'))

    except ValueError:
        flash('Invalid amount', 'danger')
        return redirect(url_for('main.main.personal'))


@bp.route('/deposit', methods=['POST'], endpoint='deposit')
@login_required
def deposit():
    amount = request.form.get('amount')
    if not amount:
        flash('Amount is required', 'danger')
        return redirect(url_for('main.main.personal'))

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError('Amount must be greater than 0')

        platform_account = PlatformAccount.query.filter_by(user_id=str(current_user.id)).first()
        bank_account = BankAccount.query.filter_by(user_id=str(current_user.id)).first()

        if bank_account.balance < amount:
            flash('Insufficient balance', 'danger')
            return redirect(url_for('main.main.personal'))

        bank_account.balance -= amount
        platform_account.balance += amount
        db.session.commit()

        flash('Deposit successfully', 'success')
        return redirect(url_for('main.main.personal'))

    except ValueError:
        flash('Invalid amount', 'danger')
        return redirect(url_for('main.main.personal'))
