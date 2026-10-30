# Cálculo de rigidez de apoyos para tuberías

Funciones en Python para estimar la rigidez (k = F/δ) de los elementos que
soportan una tubería: vigas, tirantes y ejes sometidos a torsión, así como su
combinación en serie o en paralelo.

## Unidades

| Magnitud            | Unidad      |
|---------------------|-------------|
| Fuerza              | N           |
| Longitud            | mm          |
| Módulo E, G         | N/mm² (MPa) |
| Área, inercia, J    | mm², mm⁴    |
| Rigidez lineal      | N/mm        |
| Rigidez torsional   | N·mm/rad    |

## Fórmulas implementadas

| Función                            | Caso                                        | Fórmula           |
|------------------------------------|---------------------------------------------|-------------------|
| `rigidez_voladizo`                 | Viga en voladizo, carga en el extremo       | k = 3·E·I / L³    |
| `rigidez_simple_apoyo_carga_central` | Viga simplemente apoyada, carga al centro | k = 48·E·I / L³   |
| `rigidez_empotrada_carga_central`  | Viga doblemente empotrada, carga al centro  | k = 192·E·I / L³  |
| `rigidez_barra_axial`              | Tirante o barra con carga axial             | k = E·A / L       |
| `rigidez_torsional`                | Eje o tubo en torsión                       | k_θ = G·J / L     |
| `rigidez_serie`                    | Elementos en serie                          | 1/k = Σ 1/kᵢ      |
| `rigidez_paralelo`                 | Elementos en paralelo                       | k = Σ kᵢ          |
| `desplazamiento`                   | Desplazamiento bajo una fuerza              | δ = F / k         |

Propiedades de sección: `inercia_rectangular`, `inercia_circular_maciza`,
`area_circular_maciza`, `momento_polar_anular`.

## Ejemplo: tirante con viga en serie

Un tubo DN 100 (Ø114,3 × 6 mm, acero, E = 200 000 MPa) sostenido por una viga
IPE 120 en voladizo de 1 000 mm, con un tirante de Ø16 mm y 800 mm de largo:

```python
from rigidez_apoyos import (
    area_circular_maciza, rigidez_barra_axial, rigidez_serie, rigidez_voladizo,
)

E = 200_000   # MPa
I_viga = 3_180_000  # mm⁴ (IPE 120, eje fuerte, ≈ 318 cm⁴; verificar en catálogo)
k_viga = rigidez_voladizo(E, I_viga, 1000)
k_tirante = rigidez_barra_axial(E, area_circular_maciza(16), 800)
k_apoyo = rigidez_serie(k_viga, k_tirante)
print(f"k apoyo = {k_apoyo:.1f} N/mm")
```

## Supuestos y limitaciones

- Elementos lineales y elásticos; pequeños desplazamientos.
- Cada fórmula corresponde a un caso de carga y apoyo concreto. Para otros
  casos (cargas distribuidas, apoyos elásticos, pórticos) hay que obtener la
  rigidez del modelo estructural correspondiente.
- Las propiedades de sección (I, A, J) deben tomarse del catálogo del perfil
  real. El módulo no contiene tablas de perfiles.
- Los resultados son estimaciones de preliminar; no reemplazan un análisis de
  flexibilidad ni la verificación por norma del proyecto.

## Pruebas

```bash
python -m unittest test_rigidez_apoyos -v
```
