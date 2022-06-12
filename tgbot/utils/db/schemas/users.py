class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id  = Column(BigInteger)

    query = sql.Select