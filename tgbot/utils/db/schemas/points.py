from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from tgbot.utils.db.db_helper import db


class Point(db.Model):
    __tablename__ = 'points'
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey('routes.id'))
    address = Column(String(100))
    done = Column(Boolean)
