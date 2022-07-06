from sqlalchemy import Column, Integer, BigInteger

from tgbot.utils.db.db_helper import db


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger)