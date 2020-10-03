import unittest
from .tipo_transaccion import (
    ServiceTipoTransaccion,
    TipoTransaccionDTO,
    NombreError,
    TipoTransaccion,
    Session,
)


class Test(unittest.TestCase):
    def setUp(self):
        self.service = ServiceTipoTransaccion()
        session = Session()
        self.tipos = [tipo for tipo in session.query(TipoTransaccion)]

    def test_registrar_tipo(self):
        tipo = TipoTransaccionDTO("Envio", "tipo de prueba")
        self.service.registrar_tipo(tipo)

        session = Session()
        nuevo_tipo = session.query(TipoTransaccion)[-1]
        self.assertNotEqual(nuevo_tipo.id, self.tipos[-1].id)

    def test_error_nombre(self):
        with self.assertRaises(NombreError):
            tipo = TipoTransaccionDTO("", "tipo de prueba")
            self.service.registrar_tipo(tipo)


if __name__ == "__main__":
    unittest.main()
