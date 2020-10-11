from datetime import datetime

from pytest import raises

from .recursos import TipoTransaccion, CategoriaIngreso, Ingreso
from .tipo_transaccion import (
    ServiceTipoTransaccion,
    TipoTransaccionDTO,
    NombreError,
    TipoUsoError,
)


def test_registrar_tipo(session):
    dto = TipoTransaccionDTO("Envio", "tipo de prueba")
    ServiceTipoTransaccion().registrar_tipo(dto)

    tipo = session.query(TipoTransaccion).first()
    session.close()

    assert tipo
    assert tipo.nombre == dto.nombre
    assert tipo.descripcion == dto.descripcion


def test_registrar_tipo_nombre(session):
    dto = TipoTransaccionDTO("", "tipo de prueba")

    with raises(NombreError):
        ServiceTipoTransaccion().registrar_tipo(dto)


def test_editar_tipo(session):
    tipo = TipoTransaccion(nombre="Envio", descripcion="tipo de prueba")
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    session.close()

    dto = TipoTransaccionDTO("Transporte", "tipo editado", tipo.id)
    ServiceTipoTransaccion().editar_tipo(dto)

    session.add(tipo)
    session.refresh(tipo)
    session.close()

    assert tipo.nombre == dto.nombre
    assert tipo.descripcion == dto.descripcion


def test_editar_tipo_nombre(session):
    dto = TipoTransaccionDTO("", "tipo de prueba")

    with raises(NombreError):
        ServiceTipoTransaccion().editar_tipo(dto)


def test_eliminar_tipo(session):
    tipo = TipoTransaccion(nombre="Envio", descripcion="tipo de prueba")
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    session.close()

    dto = TipoTransaccionDTO("", "", tipo.id)
    ServiceTipoTransaccion().eliminar_tipo(dto)

    tipo = session.query(TipoTransaccion).filter_by(id=tipo.id).first()
    session.close()

    assert not tipo


def test_eliminar_tipo_enUso(session):
    tipo = TipoTransaccion(nombre="Envio", descripcion="tipo de prueba")
    categoria = CategoriaIngreso(nombre="Efectivo", descripcion="categoria de prueba")
    ingreso = Ingreso(
        monto=100,
        tipo_transaccion=tipo,
        categoria=categoria,
        descripcion="ingreso de prueba",
        fecha=datetime.now(),
    )
    session.add(ingreso)
    session.commit()

    dto = TipoTransaccionDTO("", "", tipo.id)

    with raises(TipoUsoError):
        ServiceTipoTransaccion().eliminar_tipo(dto)

    session.close()


def test_obtener_tipos(session):
    tipos = [
        TipoTransaccion(nombre="Seguro", descripcion="tipo de prueba 1"),
        TipoTransaccion(nombre="Hipoteca", descripcion="tipo de prueba 2"),
        TipoTransaccion(nombre="Pension", descripcion="tipo de prueba 3"),
    ]
    session.add_all(tipos)
    session.commit()

    dtos = ServiceTipoTransaccion().obtener_tipos()

    for i, dto in enumerate(dtos):
        assert dto.id == tipos[i].id
        assert dto.nombre == tipos[i].nombre
        assert dto.descripcion == tipos[i].descripcion

    session.close()
