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
        dto = TipoTransaccionDTO("Envio", "tipo de prueba")
        ServiceTipoTransaccion().registrar_tipo(dto)

        session = Session()
        tipo = session.query(TipoTransaccion).first()
        session.close()

        self.assertIsNotNone(tipo)
        self.assertEqual(tipo.nombre, dto.nombre)
        self.assertEqual(tipo.descripcion, dto.descripcion)

    def test_registrar_tipo_nombre(self):
        with self.assertRaises(NombreError):
            dto = TipoTransaccionDTO("", "tipo de prueba")
            ServiceTipoTransaccion().registrar_tipo(dto)

    def test_editar_tipo(self):
        session = Session()
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

        self.assertEqual(tipo.nombre, dto.nombre)
        self.assertEqual(tipo.descripcion, dto.descripcion)

    def test_editar_tipo_nombre(self):
        with self.assertRaises(NombreError):
            dto = TipoTransaccionDTO("", "tipo de prueba")
            ServiceTipoTransaccion().editar_tipo(dto)

    def test_eliminar_tipo(self):
        session = Session()
        tipo = TipoTransaccion(nombre="Envio", descripcion="tipo de prueba")
        session.add(tipo)
        session.commit()
        session.refresh(tipo)
        session.close()

        dto = TipoTransaccionDTO("", "", tipo.id)
        ServiceTipoTransaccion().eliminar_tipo(dto)

        tipo = session.query(TipoTransaccion).filter_by(id=tipo.id).first()
        session.close()

        self.assertIsNone(tipo)

    def test_eliminar_tipo_enUso(self):
        with self.assertRaises(TipoUsoError):
            session = Session()
            tipo = TipoTransaccion(nombre="Envio", descripcion="tipo de prueba")
            session.add(tipo)
            session.commit()
            session.refresh(tipo)
            session.close()

            categoria = CategoriaIngreso(nombre="Efectivo", descripcion="categoria de prueba")
            session.add(categoria)
            session.commit()
            session.refresh(categoria)
            session.close()

            ingreso = Ingreso(
                    monto=100,
                    id_tipo_transaccion=tipo.id,
                    id_categoria=categoria.id,
                    descripcion="ingreso de prueba",
                    fecha=datetime.now(),
                    )
            session.add(ingreso)
            session.commit()

            dto =  TipoTransaccionDTO("", "", tipo.id)
            ServiceTipoTransaccion().eliminar_tipo(dto)

    def test_obtener_tipos(self):
        tipos = [
            TipoTransaccion(nombre="Seguro", descripcion="tipo de prueba 1"),
            TipoTransaccion(nombre="Hipoteca", descripcion="tipo de prueba 2"),
            TipoTransaccion(nombre="Pension", descripcion="tipo de prueba 3"),
        ]

        session = Session()
        session.add_all(tipos)
        session.commit()

        dtos = ServiceTipoTransaccion().obtener_tipos()

        for i, dto in enumerate(dtos):
            self.assertEqual(dto.id, tipos[i].id)
            self.assertEqual(dto.nombre, tipos[i].nombre)
            self.assertEqual(dto.descripcion, tipos[i].descripcion)

        session.close()


if __name__ == "__main__":
    unittest.main()
