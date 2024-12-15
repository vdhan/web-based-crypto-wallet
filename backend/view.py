from flask import Response, jsonify, request

from model import Chain, User, db
from util import add_wallet, check_pass, is_email
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
        chain = db.session.query(Chain).filter_by(code=2).first()
        user = User(email=email, password=pwd)
        wallet = add_wallet(pwd, app.config['SECRET_KEY'], user=user, chain=chain)

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

    user = db.session.query(User).filter_by(email=email, deleted=False).first()
    if not user:
        res = {
            'msg': 'Account not existed'
        }

        return jsonify(res), 400

    if not check_pass(pwd, user.password):
        res = {
            'msg': 'Wrong password'
        }

        return jsonify(res), 400

    res = {
        'id': user.id,
        'email': email,
        'address': user.wallets[0].address
    }

    return jsonify(res)


def manage_wallet() -> Response:
    data = {
        'msg': 'hello'
    }

    return data
