import bcrypt
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from ulid import ULID


def generate_ulid() -> str:
    return str(ULID())


def hash_password(password: str) -> str:
    byte = password.encode()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(byte, salt).decode()


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(String(26), default=generate_ulid, primary_key=True)
    created: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=datetime.now)


class User(Base):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String(60))
    actived: Mapped[bool] = mapped_column(default=False)
    deleted: Mapped[bool] = mapped_column(default=False)
    wallets: Mapped[list['Wallet']] = relationship(back_populates='user')

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = hash_password(password)

    def __str__(self):
        return f'{self.id}: {self.email}'


class Chain(Base):
    __tablename__ = 'chains'

    code: Mapped[int] = mapped_column(unique=True)
    chain: Mapped[str]
    wallets: Mapped[list['Wallet']] = relationship(back_populates='chain')

    def __str__(self):
        return f'{self.code}: {self.chain}'


class Wallet(Base):
    __tablename__ = 'wallets'

    address: Mapped[int] = mapped_column(unique=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    chain_id: Mapped[str] = mapped_column(ForeignKey('chains.id'))
    mnemonic: Mapped[str] = mapped_column(unique=True)
    tag: Mapped[str] = mapped_column(String(32))
    user: Mapped['User'] = relationship(back_populates='wallets')
    chain: Mapped['Chain'] = relationship(back_populates='wallets')

    def __str__(self):
        return f'{self.address}: {self.user_id} - {self.chain}'


class Activate(Base):
    __tablename__ = 'activate'

    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    code: Mapped[str] = mapped_column(String(8))
    user: Mapped['User'] = relationship()

    def __str__(self):
        return f'{self.user_id}: {self.code}'


db = SQLAlchemy(model_class=Base)
