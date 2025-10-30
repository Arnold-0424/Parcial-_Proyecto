from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from models.relacion import ProyectoEmpleadoLink

if TYPE_CHECKING:
    from models.proyecto import Proyecto

class Empleado(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    especialidad: str
    salario: float
    estado: bool = Field(default=True)

    # 🔗 Relación N:M con proyectos
    proyectos_link: List["ProyectoEmpleadoLink"] = Relationship(back_populates="empleado")

    # 🔗 Relación 1:N (empleado como gerente de varios proyectos)
    proyectos_gerenciados: List["Proyecto"] = Relationship(back_populates="gerente")

# ✅ Modelo para creación
class EmpleadoCreate(SQLModel):
    nombre: str
    especialidad: str
    salario: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Laura Méndez",
                    "especialidad": "Backend Developer",
                    "salario": 3500000
                }
            ]
        }
    }


# ✅ Modelo para lectura
class EmpleadoRead(SQLModel):
    id: int
    nombre: str
    especialidad: str
    salario: float
    estado: bool
