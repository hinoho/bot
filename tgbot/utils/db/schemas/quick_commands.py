async def add_user(id: int, telegram_id: int):
    try:
        user = User(id=id, telegram_id=telegram_id)

        await user.create()

    except UniqueViolationError:
        pass

async def select_all_users():
    users = await User.query.gino.all()
    return users

async def select_user(telegram_id: telegram_id):
    user = await User.query.where(User.telegram_id == telegram_id).gino.first()
    return user
