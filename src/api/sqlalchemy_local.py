from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///database/db?charset=utf8')
_SessionFactory = sessionmaker(bind=engine)
Base = declarative_base()


def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()


def add_object(instance):
    session = session_factory()
    try:
        session.add(instance)
        session.commit()
        session.close()
        return True
    except Exception as e:
        session.rollback()
        return False

def get_objects(class_name):
    session = session_factory()
    try:
        objects_query = session.query(class_name)
        session.close()
        return objects_query.all()
    except Exception as e:
        raise e