"""Cálculo de rigidez de apoyos para sistemas de tuberías.

Unidades coherentes usadas en todo el módulo:
    fuerza: N, longitud: mm, módulo elástico E y G: N/mm² (MPa),
    área: mm², momento de inercia e I/J: mm⁴, rigidez resultante: N/mm
    (o N·mm/rad para rigidez torsional).
"""
import math


def _validar_positivo(**valores):
    for nombre, valor in valores.items():
        if valor <= 0:
            raise ValueError(f"{nombre} debe ser mayor que cero (valor: {valor})")


def inercia_rectangular(b, h):
    """Momento de inercia I = b·h³/12 de una sección rectangular [mm⁴]."""
    _validar_positivo(b=b, h=h)
    return b * h**3 / 12


def area_circular_maciza(d):
    """Área A = π·d²/4 de una sección circular maciza [mm²]."""
    _validar_positivo(d=d)
    return math.pi * d**2 / 4


def inercia_circular_maciza(d):
    """Momento de inercia I = π·d⁴/64 de una sección circular maciza [mm⁴]."""
    _validar_positivo(d=d)
    return math.pi * d**4 / 64


def momento_polar_anular(D, d):
    """Momento polar J = π·(D⁴ − d⁴)/32 de un tubo de diámetro exterior D e interior d [mm⁴]."""
    _validar_positivo(D=D, d=d)
    if d >= D:
        raise ValueError("el diámetro interior d debe ser menor que el exterior D")
    return math.pi * (D**4 - d**4) / 32


def rigidez_voladizo(E, I, L):
    """Viga en voladizo con carga puntual en el extremo libre: k = 3·E·I/L³ [N/mm]."""
    _validar_positivo(E=E, I=I, L=L)
    return 3 * E * I / L**3


def rigidez_simple_apoyo_carga_central(E, I, L):
    """Viga simplemente apoyada con carga puntual al centro: k = 48·E·I/L³ [N/mm]."""
    _validar_positivo(E=E, I=I, L=L)
    return 48 * E * I / L**3


def rigidez_empotrada_carga_central(E, I, L):
    """Viga doblemente empotrada con carga puntual al centro: k = 192·E·I/L³ [N/mm]."""
    _validar_positivo(E=E, I=I, L=L)
    return 192 * E * I / L**3


def rigidez_barra_axial(E, A, L):
    """Barra o tirante sometido a carga axial: k = E·A/L [N/mm]."""
    _validar_positivo(E=E, A=A, L=L)
    return E * A / L


def rigidez_torsional(G, J, L):
    """Eje o tubo sometido a torsión: k_θ = G·J/L [N·mm/rad]."""
    _validar_positivo(G=G, J=J, L=L)
    return G * J / L


def rigidez_serie(*rigideces):
    """Rigidez equivalente de elementos en serie: 1/k = Σ 1/kᵢ [N/mm]."""
    _validar_positivo(**{f"k{i}": k for i, k in enumerate(rigideces, start=1)})
    if not rigideces:
        raise ValueError("se requiere al menos una rigidez")
    return 1 / sum(1 / k for k in rigideces)


def rigidez_paralelo(*rigideces):
    """Rigidez equivalente de elementos en paralelo: k = Σ kᵢ [N/mm]."""
    _validar_positivo(**{f"k{i}": k for i, k in enumerate(rigideces, start=1)})
    if not rigideces:
        raise ValueError("se requiere al menos una rigidez")
    return sum(rigideces)


def desplazamiento(fuerza, rigidez):
    """Desplazamiento δ = F / k bajo una fuerza dada [mm]."""
    _validar_positivo(rigidez=rigidez)
    return fuerza / rigidez
