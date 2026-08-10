from dataclasses import dataclass
from datetime import date
from typing import Optional

ESTADOS_VALIDOS = ("bueno", "usado", "para_desecho")


@dataclass
class InventarioNeumatico:
    inventario_id: int
    vulcanizadora_id: int
    tipo_neumatico: str
    medida: str
    marca: str
    cantidad: int
    estado: str
    fecha_ingreso: date
    observaciones: Optional[str] = None

    def __post_init__(self):
        if self.estado not in ESTADOS_VALIDOS:
            raise ValueError(
                f"estado inválido '{self.estado}', debe ser uno de {ESTADOS_VALIDOS}"
            )
        if self.cantidad < 0:
            raise ValueError("cantidad no puede ser negativa")


@dataclass
class InventarioNeumaticoNuevo:

    vulcanizadora_id: int
    tipo_neumatico: str
    medida: str
    marca: str
    cantidad: int
    estado: str
    observaciones: Optional[str] = None
