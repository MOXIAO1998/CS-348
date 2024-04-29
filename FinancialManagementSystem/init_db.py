from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()

    from app.models import User
    user = User(username='user1', email='user1@qq.com')
    user.set_password('user1')
    db.session.add(user)

    user = User(username='user2', email='user2@qq.com')
    user.set_password('user2')
    db.session.add(user)

    user = User(username='user3', email='user3@qq.com')
    user.set_password('user3')
    db.session.add(user)

    db.session.commit()

    from app.models import Stock

    stock = Stock(symbol='A00001', name='A00001')
    db.session.add(stock)

    stock = Stock(symbol='A00002', name='A00002')
    db.session.add(stock)

    stock = Stock(symbol='A00003', name='A00003')
    db.session.add(stock)

    stock = Stock(symbol='A00004', name='A00004')
    db.session.add(stock)

    stock = Stock(symbol='A00005', name='A00005')
    db.session.add(stock)

    db.session.commit()

    from app.models import BankAccount, PlatformAccount

    bank_account = BankAccount(user_id=1, bank_name='bank1', balance=10000)
    db.session.add(bank_account)

    bank_account = BankAccount(user_id=2, bank_name='bank2', balance=20000)
    db.session.add(bank_account)

    bank_account = BankAccount(user_id=3, bank_name='bank3', balance=300000)
    db.session.add(bank_account)

    db.session.commit()

    platform_account = PlatformAccount(user_id=1, balance=100000)
    db.session.add(platform_account)

    platform_account = PlatformAccount(user_id=2, balance=200000)
    db.session.add(platform_account)

    platform_account = PlatformAccount(user_id=3, balance=30000)
    db.session.add(platform_account)

    db.session.commit()

    from app.models import UserStock

    user_stock = UserStock(user_id=1, stock_id=1, quantity=100)
    db.session.add(user_stock)

    user_stock = UserStock(user_id=1, stock_id=2, quantity=200)
    db.session.add(user_stock)

    user_stock = UserStock(user_id=1, stock_id=4, quantity=400)
    db.session.add(user_stock)

    user_stock = UserStock(user_id=1, stock_id=5, quantity=500)
    db.session.add(user_stock)

    db.session.commit()

    user_stock = UserStock(user_id=2, stock_id=1, quantity=100)
    db.session.add(user_stock)

    user_stock = UserStock(user_id=2, stock_id=2, quantity=200)
    db.session.add(user_stock)

    user_stock = UserStock(user_id=2, stock_id=4, quantity=400)
    db.session.add(user_stock)

    user_stock = UserStock(user_id=2, stock_id=5, quantity=500)
    db.session.add(user_stock)

    db.session.commit()







