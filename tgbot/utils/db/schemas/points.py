class Point(TimedBaseModel):
    __tablename__ = 'points'
    id = Column(Integer, primary_key=True)
    route_id  = Column(Integer)
    address = Column(String(100))

    query = sql.Select