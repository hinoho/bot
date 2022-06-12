class Route(TimedBaseModel):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True)
    user_id  = Column(Integer)

    query = sql.Select