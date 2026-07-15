from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional

@dataclass(frozen = True)

class Usuario :
    id_usuario: Optional[int] = None
    username: str = field(default = "")
    password_hash: str = field(default = "")
    nombre: str = field(default = "")
    aPaterno: str = field(default = "")
    aMaterno: str = field(default = "")
    rol: str = field(default = "operador")
    activo: bool = True
    creado_en: datetime = field(default_factory = datetime.now)
    ultimo_acceso: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto Usuario a un diccionario para su almacenamiento en la base de datos."""
        return {
            "id_usuario": self.id_usuario,
            "username": self.username,
            "password_hash": self.password_hash,
            "nombre": self.nombre,
            "aPaterno": self.aPaterno,
            "aMaterno": self.aMaterno,
            "rol": self.rol,
            "activo": self.activo,
            "creado_en": self.creado_en.isoformat() if self.creado_en else None,
            "ultimo_acceso": self.ultimo_acceso.isoformat() if self.ultimo_acceso else None
        }

    @classmethod
    def from_dict (cls, data: Dict[str, Any]) -> "Usuario":

        #Limpiar fecha si viene en formato string desde la base de datos o aplicacion externa
        creado_en_raw = data.get("creado_en")
        if isinstance(creado_en_raw, str):
            creado_en = datetime.fromisoformat(creado_en_raw)
        elif isinstance(creado_en_raw, datetime):
            creado_en = creado_en_raw
        else:
            creado_en = datetime.now()

        ultimo_acceso_raw = data.get("ultimo_acceso")
        ultimo_acceso = None

        if isinstance(ultimo_acceso_raw, str):
            ultimo_acceso = datetime.fromisoformat(ultimo_acceso_raw)
        elif isinstance(ultimo_acceso_raw, datetime):
            ultimo_acceso = ultimo_acceso_raw


        return cls (
            id_usuario = data.get("id_usuario"),
            username = str(data.get("username", "")),
            password_hash = str(data.get("password_hash", "")),
            nombre = str(data.get("nombre", "")),
            aPaterno = str(data.get("aPaterno", "")),
            aMaterno = str(data.get("aMaterno", "")),
            rol = str(data.get("rol", "operador")),
            activo = bool(data.get("activo", True)),
            creado_en = creado_en,
            ultimo_acceso = ultimo_acceso
        )