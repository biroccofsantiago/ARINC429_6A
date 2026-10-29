import unittest
from unittest.mock import MagicMock, patch

import app


class InstrumentosTest(unittest.TestCase):
    def setUp(self):
        self.cursor = MagicMock()
        self.conexion = MagicMock()
        self.conexion.cursor.return_value = self.cursor
        patcher = patch("app.conectar", return_value=self.conexion)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_crear_instrumento(self):
        app.crear_instrumento(" Altímetro ")

        self.cursor.execute.assert_called_once_with(
            "INSERT INTO instrumentos (ins_descripcion) VALUES (%s)",
            ("Altímetro",),
        )
        self.conexion.commit.assert_called_once_with()
        self.cursor.close.assert_called_once_with()
        self.conexion.close.assert_called_once_with()

    def test_actualizar_instrumento(self):
        self.cursor.rowcount = 1

        app.actualizar_instrumento(3, "Radioaltímetro")

        self.cursor.execute.assert_called_once_with(
            "UPDATE instrumentos SET ins_descripcion = %s WHERE ins_id = %s",
            ("Radioaltímetro", 3),
        )
        self.conexion.commit.assert_called_once_with()

    def test_eliminar_instrumento(self):
        self.cursor.rowcount = 1

        app.eliminar_instrumento(3)

        self.cursor.execute.assert_called_once_with(
            "DELETE FROM instrumentos WHERE ins_id = %s", (3,)
        )
        self.conexion.commit.assert_called_once_with()

    def test_listar_instrumentos(self):
        self.cursor.fetchall.return_value = [(3, "Altímetro")]

        with patch("builtins.print") as imprimir:
            app.listar_instrumentos()

        self.cursor.execute.assert_called_once_with(
            "SELECT ins_id, ins_descripcion FROM instrumentos ORDER BY ins_id"
        )
        imprimir.assert_any_call("ID: 3 | Descripción: Altímetro")

    def test_rechaza_descripcion_vacia_o_mayor_a_50_caracteres(self):
        for descripcion in ("  ", "x" * 51):
            with self.subTest(descripcion=descripcion), self.assertRaises(ValueError):
                app.crear_instrumento(descripcion)


if __name__ == "__main__":
    unittest.main()
