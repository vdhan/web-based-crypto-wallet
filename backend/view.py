from flask import Response, jsonify, request

from model import User, db
from util import is_valid_email


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

    if not is_valid_email(str(email)):
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

    result = db.session.query(User).filter_by(email=email).first()
    # TODO: check if deleted
    if result:
        res = {
            'msg': 'Email existed'
        }

        return jsonify(res), 400

    # TODO: active and create wallet separately
    user = User(email=email, password=pwd)
    db.session.add(user)
    db.session.commit()

    res = {
        'id': user.id,
        'email': email
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
