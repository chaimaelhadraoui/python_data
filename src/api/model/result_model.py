import datetime
from sqlalchemy import Column, Integer, VARCHAR
from src.api.sqlalchemy_local import Base


class Result(Base):
    __tablename__ = 'result'

    id_result = Column(Integer, primary_key=True, autoincrement=True)
    result = Column(VARCHAR(250), nullable=True)

    def __repr__(self):
        return str({'id_result': self.id_result, 'result': self.result})