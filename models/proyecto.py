from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from models.relacion import ProyectoEmpleadoLink

if TYPE_CHECKING:
    from models.empleado import Empleado

class Proyecto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    presupuesto: float
    estado: bool = Field(default=True)
    gerente_id: Optional[int] = Field(default=None, foreign_key="empleado.id")

    # 🔗 Relación N:M con empleados
    empleados_link: List["ProyectoEmpleadoLink"] = Relationship(back_populates="proyecto")

    # 🔗 Relación 1:N con gerente
    gerente: Optional["Empleado"] = Relationship(back_populates="proyectos_gerenciados")


# ✅ Modelo para creación
class ProyectoCreate(SQLModel):
    nombre: str
    descripcion: str
    presupuesto: float
    estado: bool = True
    gerente_id: Optional[int] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Optimización Eólica",
                    "descripcion": "Proyecto para desarrollar generador eólico de bajo costo",
                    "presupuesto": 10000000,
                    "estado": True,
                    "gerente_id": 1
                }
            ]
        }
    }
