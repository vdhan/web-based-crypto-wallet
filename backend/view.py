from collections import OrderedDict
from flask import Response, jsonify, request

from model import Chain, User, db
from util import add_wallet, check_pass, is_email
from wsgi import app


def signup() -> Response:
    data: dict = request.get_json()
    email = data.get('email')
    if email is None:
        res = OrderedDict([
            ('msg', 'Email must not empty')
        ])

        return jsonify(res), 400

    pwd = data.get('password')
    if pwd is None:
        res = OrderedDict([
            ('msg', 'Password must not empty')
        ])

        return jsonify(res), 400

    if not is_email(str(email)):
        res = OrderedDict([
            ('msg', 'Invalid email')
        ])

        return jsonify(res), 400

    pwd = str(pwd).strip()
    if len(pwd) == 0:
        res = OrderedDict([
            ('msg', 'Empty password')
        ])

        return jsonify(res), 400

    user = db.session.query(User).filter_by(email=email).first()
    if user and user.deleted is False:
        res = OrderedDict([
            ('msg', 'Email existed')
        ])

        return jsonify(res), 400
    elif user and user.deleted is True:
        user.deleted = False
    else:
        chain = db.session.query(Chain).filter_by(code=2).first()
        user = User(email=email, password=pwd)
        wallet = add_wallet(pwd, app.config['SALT'], user=user, chain_id=chain.id)

        db.session.add(user)
        db.session.add(wallet)

    db.session.commit()
    res = OrderedDict([
        ('id', user.id),
        ('email', email),
        ('address', wallet.address)
    ])

    return jsonify(res)


def login() -> Response:
    data: dict = request.get_json()
    email = data.get('email')
    if email is None:
        res = OrderedDict([
            ('msg', 'Email must not empty')
        ])

        return jsonify(res), 400

    pwd = data.get('password')
    if pwd is None:
        res = OrderedDict([
            ('msg', 'Password must not empty')
        ])

        return jsonify(res), 400

    if not is_email(str(email)):
        res = OrderedDict([
            ('msg', 'Invalid email')
        ])

        return jsonify(res), 400

    user = db.session.query(User).filter_by(email=email, deleted=False).first()
    if not user:
        res = OrderedDict([
            ('msg', 'Account not existed')
        ])

        return jsonify(res), 400

    if not check_pass(pwd, user.password):
        res = OrderedDict([
            ('msg', 'Wrong password')
        ])

        return jsonify(res), 400

    wallets = []
    for item in user.wallets:
        wallet = OrderedDict([
            ('chain', item.chain.chain),
            ('address', item.address)
        ])

        wallets.append(wallet)

    res = OrderedDict([
        ('id', user.id),
        ('email', email),
        ('wallets', wallets)
    ])

    return jsonify(res)
