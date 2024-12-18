# Web based Crypto Wallet
Web based crypto wallet.

## Setup
1. Clone this repository to your local machine.
2. Install Python <= 3.11
3. Go to `ROOT_PROJECT` and create Python virtual environment:
```shell
python -m venv env
```

4. Install requirements:
```shell
source env/bin/activate
pip install -r requirements.txt
```

5. Generate `SECRET_KEY`:
```shell
python -c 'import secrets; print(secrets.token_hex())'
```

6. Generate `SALT`:
```shell
python -c 'import secrets; print(secrets.token_hex(16))'
```

7. Create new file `.env` with content:
```shell
SECRET_KEY=SECRET_KEY
SALT=SALT
```

8. Create folder `ROOT_PROJECT/key`, then go into it and generate RSA key:
```shell
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem
```

9. Go to folder `ROOT_PROJECT/backend`, initialize database:
```shell
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

10. Go to folder `ROOT_PROJECT/frontend`, install frontend dependencies:
```shell
npm install
```

## Start
1. Go to folder `ROOT_PROJECT/frontend`, run frontend server:
```shell
npm run start
```

Leave the terminal open

2. Go to folder `ROOT_PROJECT/backend`, run backend server:
```shell
python wsgi.py
```

Leave the terminal open, too

## Developing
Each time the database models change, repeat the `migrate` and `upgrade` commands:
```shell
flask db migrate
flask db upgrade
```

## Future Feature
- Deploy on cloud (BizFly Cloud, Clearsky, etc.) for production.
- Expand features (logging, etc.), make it become full fledged wallet.
- Integrate multi chain for cross chain transaction.
- Run cron for cleaning database automatically