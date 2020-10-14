from pytest import fixture

from app.modelo.recursos import Base, engine, Session, TipoTransaccion


@fixture()
def session():
    Base.metadata.create_all(engine)
    yield Session()
    Base.metadata.drop_all(engine)
    

@fixture()
def tipo():
    return TipoTransaccion(nombre="Envio", descripcion="tipo de prueba") 