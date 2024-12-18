from collections import OrderedDict
from pathlib import Path
from flask import Response, jsonify, request

from model import Chain, User, Wallet
from util import check_pass, decode_rsa_token, encrypt, gen_address, gen_mnemonic, gen_rsa_token, is_email
from wsgi import app, db


def add_wallet(password: str, salt: str, **kw) -> Wallet:
    nemo = gen_mnemonic()
    address = gen_address(nemo)
    nemo, tag = encrypt(nemo, password, salt)
    return Wallet(address=address, mnemonic=nemo, tag=tag, **kw)


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

    key_path: Path = app.config['BASE_DIR'] / 'key/private.pem'
    token = gen_rsa_token(app.config['ISS'], user.id, key_path)
    res = OrderedDict([
        ('token', token)
    ])

    return jsonify(res)


def wallet_cardano() -> Response:
    auth_head = request.headers.get('Authorization')
    if not auth_head:
        res = OrderedDict([
            ('msg', 'Missing token')
        ])

        return jsonify(res), 401

    try:
        key_path: Path = app.config['BASE_DIR'] / 'key/public.pem'
        token = auth_head.split(' ')[1]
        decoded = decode_rsa_token(token, key_path)
        if 'error' in decoded:
            res = OrderedDict([
                ('msg', decoded['error'])
            ])

            return jsonify(res), 401

        issue = decoded.get('iss', '')
        if issue != app.config['ISS']:
            res = OrderedDict([
                ('msg', 'Invalid issuer')
            ])

            return jsonify(res), 401

        sub = decoded.get('sub')
        if not sub:
            res = OrderedDict([
                ('msg', 'Invalid user')
            ])

            return jsonify(res), 401

        user = db.session.query(User).filter_by(id=sub, deleted=False).first()
        if not user:
            res = OrderedDict([
                ('msg', 'User not existed')
            ])

            return jsonify(res), 401

        wallets = []
        for item in user.wallets:
            wallet = OrderedDict([
                ('chain', item.chain.chain),
                ('address', item.address)
            ])

            wallets.append(wallet)

        res = OrderedDict([
            ('wallets', wallets)
        ])

        return jsonify(res)
    except IndexError:
        res = OrderedDict([
            ('msg', 'Invalid Authorization header')
        ])

        return jsonify(res), 401
