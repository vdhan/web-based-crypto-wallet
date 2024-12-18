import bcrypt
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from util import gen_ulid


def hash_pass(password: str) -> str:
    byte = password.encode()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(byte, salt).decode()


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(String(26), default=gen_ulid, primary_key=True)
    created: Mapped[datetime] = mapped_column(default=datetime.now)


class Updatable:
    updated: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)


class User(Base, Updatable):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String(60))
    actived: Mapped[bool] = mapped_column(default=False)
    deleted: Mapped[bool] = mapped_column(default=False)
    wallets: Mapped[list['Wallet']] = relationship(back_populates='user')

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = hash_pass(password)

    def __str__(self) -> str:
        return f'{self.id}: {self.email}'


class Chain(Base, Updatable):
    __tablename__ = 'chains'

    code: Mapped[int] = mapped_column(unique=True)
    chain: Mapped[str]
    wallets: Mapped[list['Wallet']] = relationship(back_populates='chain')

    def __str__(self) -> str:
        return f'{self.code}: {self.chain}'


class Wallet(Base, Updatable):
    __tablename__ = 'wallets'

    address: Mapped[int] = mapped_column(unique=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    chain_id: Mapped[str] = mapped_column(ForeignKey('chains.id'))
    mnemonic: Mapped[str] = mapped_column(unique=True)
    tag: Mapped[str] = mapped_column(String(32))
    user: Mapped['User'] = relationship(back_populates='wallets')
    chain: Mapped['Chain'] = relationship(back_populates='wallets')

    def __str__(self) -> str:
        return f'{self.address}: {self.user_id} - {self.chain}'


class Activate(Base):
    __tablename__ = 'activate'

    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    code: Mapped[str] = mapped_column(String(8))
    till: Mapped[datetime]
    actived: Mapped[bool] = mapped_column(default=False)
    user: Mapped['User'] = relationship()

    def __str__(self) -> str:
        return f'{self.user_id}: {self.code}'


class Revoke(Base):
    __tablename__ = 'revoke'

    jti: Mapped[str] = mapped_column(String(26))
    expire: Mapped['datetime']

    def __str__(self) -> str:
        return f'{self.jti}: {self.expire}'


db = SQLAlchemy(model_class=Base)
