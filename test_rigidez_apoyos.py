import math
import unittest

from rigidez_apoyos import (
    area_circular_maciza,
    desplazamiento,
    inercia_circular_maciza,
    inercia_rectangular,
    momento_polar_anular,
    rigidez_barra_axial,
    rigidez_empotrada_carga_central,
    rigidez_paralelo,
    rigidez_serie,
    rigidez_simple_apoyo_carga_central,
    rigidez_torsional,
    rigidez_voladizo,
)

E = 200_000  # MPa, acero
G = 80_000   # MPa, acero


class PropiedadesSeccion(unittest.TestCase):
    def test_inercia_rectangular(self):
        self.assertAlmostEqual(inercia_rectangular(10, 20), 10 * 20**3 / 12)

    def test_area_y_inercia_circular(self):
        self.assertAlmostEqual(area_circular_maciza(20), math.pi * 100)
        self.assertAlmostEqual(inercia_circular_maciza(20), math.pi * 20**4 / 64)

    def test_momento_polar_anular(self):
        self.assertAlmostEqual(momento_polar_anular(20, 10), math.pi * (20**4 - 10**4) / 32)

    def test_diametro_interior_mayor_falla(self):
        with self.assertRaises(ValueError):
            momento_polar_anular(10, 10)


class RigidezVigas(unittest.TestCase):
    def test_voladizo(self):
        self.assertAlmostEqual(rigidez_voladizo(E, 1e6, 1000), 600)

    def test_simple_apoyo_carga_central(self):
        self.assertAlmostEqual(rigidez_simple_apoyo_carga_central(E, 1e6, 1000), 9600)

    def test_empotrada_carga_central(self):
        self.assertAlmostEqual(rigidez_empotrada_carga_central(E, 1e6, 1000), 38400)

    def test_voladizo_es_mas_flexible_que_apoyo_simple(self):
        k_vol = rigidez_voladizo(E, 1e6, 1000)
        k_simple = rigidez_simple_apoyo_carga_central(E, 1e6, 1000)
        self.assertLess(k_vol, k_simple)

    def test_rigidez_inversamente_proporcional_a_L3(self):
        k1 = rigidez_voladizo(E, 1e6, 1000)
        k2 = rigidez_voladizo(E, 1e6, 2000)
        self.assertAlmostEqual(k1 / k2, 8)


class RigidezBarrasYTorsion(unittest.TestCase):
    def test_barra_axial(self):
        self.assertAlmostEqual(rigidez_barra_axial(E, 100, 1000), 20_000)

    def test_torsional(self):
        self.assertAlmostEqual(rigidez_torsional(G, 2e5, 500), G * 2e5 / 500)


class Combinaciones(unittest.TestCase):
    def test_serie_dos_iguales(self):
        self.assertAlmostEqual(rigidez_serie(600, 600), 300)

    def test_serie_siempre_menor_que_minimo(self):
        self.assertLess(rigidez_serie(600, 20_000), 600)

    def test_paralelo(self):
        self.assertAlmostEqual(rigidez_paralelo(600, 400), 1000)

    def test_tirante_mas_viga_en_serie(self):
        k_viga = rigidez_voladizo(E, 1e6, 1000)
        k_tirante = rigidez_barra_axial(E, 100, 1000)
        k_total = rigidez_serie(k_viga, k_tirante)
        self.assertAlmostEqual(k_total, 1 / (1 / k_viga + 1 / k_tirante))
        self.assertLess(k_total, min(k_viga, k_tirante))

    def test_serie_sin_argumentos_falla(self):
        with self.assertRaises(ValueError):
            rigidez_serie()

    def test_paralelo_con_rigidez_no_positiva_falla(self):
        with self.assertRaises(ValueError):
            rigidez_paralelo(600, 0)


class Validaciones(unittest.TestCase):
    def test_longitud_cero_falla(self):
        with self.assertRaises(ValueError):
            rigidez_voladizo(E, 1e6, 0)

    def test_modulo_negativo_falla(self):
        with self.assertRaises(ValueError):
            rigidez_barra_axial(-E, 100, 1000)

    def test_desplazamiento(self):
        self.assertAlmostEqual(desplazamiento(1200, 600), 2)


if __name__ == "__main__":
    unittest.main()
