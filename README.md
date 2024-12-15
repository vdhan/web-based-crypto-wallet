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

5. Generate `secret_key`:
```shell
python -c 'import secrets; print(secrets.token_hex())'
```

6. Create new file `.env` with content:
```shell
SECRET_KEY=secret_key
```

7. Go to folder `ROOT_PROJECT/frontend`, then run:
```shell
npm install
```

## Start
1. Go to folder `ROOT_PROJECT/frontend`, then run:
```shell
npm run start
```

Leave the terminal open

2. Go to folder `ROOT_PROJECT/backend`, then run:
```shell
python wsgi.py
```

Leave the terminal open, too

## Future Feature
- Deploy on cloud (BizFly Cloud, Clearsky, etc.) for production.
- Expand features (logging, etc.), make it become full fledged wallet.
- Integrate multi chain for cross chain transaction.
- Develop ecosystem: Layer-2, Payment Gateway, etc.