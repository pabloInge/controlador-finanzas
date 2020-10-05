import unittest
from datetime import datetime

from .recursos import engine, Session, Base, TipoTransaccion, CategoriaIngreso, Ingreso
from .tipo_transaccion import (
    ServiceTipoTransaccion,
    TipoTransaccionDTO,
    NombreError,
    TipoUsoError,
)


class Test(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_registrar_tipo(self):
        nuevo_tipo = TipoTransaccionDTO("Envio", "tipo de prueba")
        ServiceTipoTransaccion().registrar_tipo(nuevo_tipo)

        session = Session()
        tipo_registrado = session.query(TipoTransaccion).first()
        session.close()

        self.assertIsNotNone(tipo_registrado)
        self.assertEqual(tipo_registrado.nombre, nuevo_tipo.nombre)
        self.assertEqual(tipo_registrado.descripcion, nuevo_tipo.descripcion)

    def test_registrar_tipo_nombre(self):
        with self.assertRaises(NombreError):
            nuevo_tipo = TipoTransaccionDTO("", "tipo de prueba")
            ServiceTipoTransaccion().registrar_tipo(nuevo_tipo)

    def test_editar_tipo(self):
        session = Session()
        session.add(
            TipoTransaccion(id=None, nombre="Envio", descripcion="tipo de prueba")
        )
        session.commit()
        id_tipo_registrado = session.query(TipoTransaccion.id).scalar()
        session.close()

        tipo_editado = TipoTransaccionDTO(
            "Transporte", "tipo editado", id_tipo_registrado
        )
        ServiceTipoTransaccion().editar_tipo(tipo_editado)
        tipo_modificado = session.query(TipoTransaccion).first()
        session.close()

        self.assertEqual(id_tipo_registrado, tipo_modificado.id)
        self.assertEqual(tipo_editado.nombre, tipo_modificado.nombre)
        self.assertEqual(tipo_editado.descripcion, tipo_modificado.descripcion)

    def test_editar_tipo_nombre(self):
        with self.assertRaises(NombreError):
            tipo_editado = TipoTransaccionDTO("", "tipo de prueba")
            ServiceTipoTransaccion().editar_tipo(tipo_editado)

    def test_eliminar_tipo(self):
        session = Session()
        session.add(
            TipoTransaccion(id=None, nombre="Envio", descripcion="tipo de prueba")
        )
        session.commit()
        id_tipo_registrado = session.query(TipoTransaccion.id).scalar()
        session.close()

        ServiceTipoTransaccion().eliminar_tipo(
            TipoTransaccionDTO("", "", id_tipo_registrado)
        )
        tipos = session.query(TipoTransaccion)
        session.close()

        self.assertIsNotNone(tipos)

    def test_eliminar_tipo_enUso(self):
        with self.assertRaises(TipoUsoError):
            session = Session()
            session.add(
                TipoTransaccion(id=None, nombre="Envio", descripcion="tipo de prueba")
            )
            session.commit()
            id_tipo_registrado = session.query(TipoTransaccion.id).scalar()
            session.close()

            session.add(
                CategoriaIngreso(
                    id=None, nombre="Efectivo", descripcion="categoria de prueba"
                )
            )
            session.commit()
            id_categoria_registrada = session.query(CategoriaIngreso.id).scalar()
            session.close()

            session.add(
                Ingreso(
                    id=None,
                    monto=100,
                    id_tipo_transaccion=id_tipo_registrado,
                    id_categoria=id_categoria_registrada,
                    descripcion="ingreso de prueba",
                    fecha=datetime.now(),
                )
            )
            session.commit()

            ServiceTipoTransaccion().eliminar_tipo(
                TipoTransaccionDTO("", "", id_tipo_registrado)
            )

    def test_obtener_tipos(self):
        tipos = [
            TipoTransaccion(id=None, nombre="Seguro", descripcion="tipo de prueba 1"),
            TipoTransaccion(id=None, nombre="Hipoteca", descripcion="tipo de prueba 2"),
            TipoTransaccion(id=None, nombre="Pension", descripcion="tipo de prueba 3"),
        ]

        session = Session()
        session.add_all(tipos)
        session.commit()

        tipos_registrados = ServiceTipoTransaccion().obtener_tipos()

        for i, tipo_registrado in enumerate(tipos_registrados):
            self.assertEqual(tipo_registrado.id, tipos[i].id)
            self.assertEqual(tipo_registrado.nombre, tipos[i].nombre)
            self.assertEqual(tipo_registrado.descripcion, tipos[i].descripcion)


if __name__ == "__main__":
    unittest.main()
