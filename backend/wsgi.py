import os

from flask import Flask

from model import Chain, db


def init_db() -> None:
    with app.app_context():
        db.init_app(app)
        db.create_all()

        chain = db.session.query(Chain).first()
        if not chain:
            chains = [
                Chain(code=1, chain='Cardano Mainnet'),
                Chain(code=2, chain='Cardano Preprod')
            ]

            db.session.add_all(chains)
            db.session.commit()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wallet.db'

if __name__ == '__main__':
    import view

    init_db()

    app.add_url_rule('/signup', view_func=view.signup, methods=['POST'])
    app.add_url_rule('/login', view_func=view.login, methods=['POST'])
    app.add_url_rule('/wallet/cardano', view_func=view.manage_wallet, methods=['GET', 'POST', 'PUT', 'DELETE'])

    host = os.environ.get('HOST', '0.0.0.0')
    port = os.environ.get('PORT', 5000)
    debug = os.environ.get('DEBUG', True)
    app.run(host, port, debug)
