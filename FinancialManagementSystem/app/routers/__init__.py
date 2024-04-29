from flask import blueprints, redirect, url_for
from .auth import bp as auth_bp
from .main import bp as main_bp
from .bank import bp as bank_bp
from .stock import bp as stock_bp

bp = blueprints.Blueprint('main', __name__)


@bp.route('/', endpoint='index')
def index():
    return redirect(url_for('main.auth.login'))


bp.register_blueprint(auth_bp)

bp.register_blueprint(main_bp)

bp.register_blueprint(bank_bp)

bp.register_blueprint(stock_bp)
