import os

from flask import Flask
from dotenv import load_dotenv

import view

if __name__ == '__main__':
    load_dotenv()
    host = os.getenv('HOST', '0.0.0.0')
    port = os.getenv('PORT', 5000)
    debug = os.getenv('DEBUG', True)

    app = Flask(__name__)
    app.add_url_rule('/', view_func=view.dashboard)
    app.add_url_rule('/signup', view_func=view.signup, methods=['POST'])
    app.add_url_rule('/login', view_func=view.login, methods=['POST'])
    app.add_url_rule('/wallet/cardano', view_func=view.send_cardano, methods=['GET', 'POST', 'PUT', 'DELETE'])
    app.add_url_rule('/send/cardano', view_func=view.send_cardano, methods=['POST'])
    app.run(host, port, debug)
