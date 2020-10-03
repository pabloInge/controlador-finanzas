import unittest
from .tipo_transaccion import ServiceTipoTransaccion, TipoTransaccionDTO, NombreError


service = ServiceTipoTransaccion()


class Test(unittest.TestCase):
    def test_registrar_tipo(self):
        tipo = TipoTransaccionDTO("Envio", "tipo de prueba")
        self.assertIsNone(service.registrar_tipo(tipo))

        with self.assertRaises(NombreError):
            tipo = TipoTransaccionDTO("", "tipo de prueba")
            self.assertIsNone(service.registrar_tipo(tipo))


if __name__ == "__main__":
    unittest.main()
