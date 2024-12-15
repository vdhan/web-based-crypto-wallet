from flask import Response, jsonify, request

from model import User, db
from util import add_wallet, is_email
from wsgi import app


def signup() -> Response:
    data: dict = request.get_json()
    email = data.get('email')
    if email is None:
        res = {
            'msg': 'Email must not empty'
        }

        return jsonify(res), 400

    pwd = data.get('password')
    if pwd is None:
        res = {
            'msg': 'Password must not empty'
        }

        return jsonify(res), 400

    if not is_email(str(email)):
        res = {
            'msg': 'Invalid email'
        }

        return jsonify(res), 400

    pwd = str(pwd).strip()
    if len(pwd) == 0:
        res = {
            'msg': 'Empty password'
        }

        return jsonify(res), 400

    user = db.session.query(User).filter_by(email=email).first()
    if user and user.deleted is False:
        res = {
            'msg': 'Email existed'
        }

        return jsonify(res), 400
    elif user and user.deleted is True:
        user.deleted = False
    else:
        user = User(email=email, password=pwd)
        wallet = add_wallet(pwd, app.config['SECRET_KEY'], chain_id=2, user=user)
        db.session.add(user)
        db.session.add(wallet)

    db.session.commit()
    res = {
        'id': user.id,
        'email': email,
        'address': wallet.address
    }

    return jsonify(res)


def login() -> Response:
    data = {
        'msg': 'hello'
    }

    return data


def manage_wallet() -> Response:
    data = {
        'msg': 'hello'
    }

    return data
