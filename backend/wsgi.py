import os

from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)
if __name__ == '__main__':
    import view
    from model import db

    load_dotenv()
    host = os.getenv('HOST', '0.0.0.0')
    port = os.getenv('PORT', 5000)
    debug = os.getenv('DEBUG', True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wallet.db'
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.add_url_rule('/signup', view_func=view.signup, methods=['POST'])
    app.add_url_rule('/login', view_func=view.login, methods=['POST'])
    app.add_url_rule('/wallet/cardano', view_func=view.manage_wallet, methods=['GET', 'POST', 'PUT', 'DELETE'])
    app.run(host, port, debug)
