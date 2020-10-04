import unittest

from sqlalchemy import MetaData

from .recursos import engine, TipoTransaccion, Session, Base
from .tipo_transaccion import (
    ServiceTipoTransaccion,
    TipoTransaccionDTO,
    NombreError,
)


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engine.execute("DROP DATABASE finanzas")
        engine.execute("CREATE DATABASE finanzas")
        engine.execute("USE finanzas")
        Base.metadata.create_all(engine)
        cls.service = ServiceTipoTransaccion()

    def test_registrar_tipo(self):
        nuevo_tipo = TipoTransaccionDTO("Envio", "tipo de prueba")
        self.service.registrar_tipo(nuevo_tipo)

        session = Session()
        tipo = session.query(TipoTransaccion).first()

        self.assertIsNotNone(tipo)
        with self.subTest():
            self.assertEqual(tipo.nombre, nuevo_tipo.nombre)
        with self.subTest():
            self.assertEqual(tipo.descripcion, nuevo_tipo.descripcion)
    
    def test_error_nombre(self):
        with self.assertRaises(NombreError):
            nuevo_tipo = TipoTransaccionDTO("", "tipo de prueba")
            self.service.registrar_tipo(nuevo_tipo)


if __name__ == "__main__":
    unittest.main()
