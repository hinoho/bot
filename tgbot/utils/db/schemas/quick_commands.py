import numpy as np
from sqlalchemy import desc

from tgbot.utils.db.schemas.points import Point
from tgbot.utils.db.schemas.routes import Route
from tgbot.utils.db.schemas.users import User
from asyncpg import UniqueViolationError


async def add_user(telegram_id: int):
    try:
        user = User(telegram_id=telegram_id)
        await user.create()
        return user.id
    except UniqueViolationError:
        pass


async def add_points(user_id: int, points: list):
    route = Route(user_id=user_id)
    await route.create()

    for point in points:
        row = Point(route_id=route.id, address=point, done=False)
        await row.create()


async def select_all_users():
    users = await User.select('telegram_id').gino.all()
    return np.asarray(users)


async def select_user(telegram_id: int):
    user = await User.query.where(User.telegram_id == telegram_id).gino.first()
    return user


async def get_points(user_id: int):
    route = await Route.query.where(Route.user_id == user_id).gino.first()
    points = await Point.query.where(Point.route_id == route.id).order_by(Point.id).gino.all()

    return points


async def get_next_point(user_id: int):
    route = await Route.query.where(Route.user_id == user_id).gino.first()
    point = await Point.query.where(Point.route_id == route.id).where(Point.done == False).order_by(Point.id).gino.all()
    if point:
        return point[0]
    return None


async def update_point(user_id: int):
    route = await Route.query.where(Route.user_id == user_id).gino.first()
    point = await Point.query.where(Point.route_id == route.id).where(Point.done == False).gino.first()
    await point.update(done=True).apply()

    return point
