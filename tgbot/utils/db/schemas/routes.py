from tgbot.utils.db.db_helper import db
from sqlalchemy import Column, Integer, ForeignKey


class Route(db.Model):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
