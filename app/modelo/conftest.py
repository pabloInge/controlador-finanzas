from pytest import fixture
from .recursos import Base, engine, Session


@fixture()
def session():
    Base.metadata.create_all(engine)
    yield Session()
    Base.metadata.drop_all(engine)
    