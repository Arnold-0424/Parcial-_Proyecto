from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING # noqa: F401

if TYPE_CHECKING:
    from models.empleado import Empleado

class Proyecto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    presupuesto: float
    estado: bool = Field(default=True)  # 👈 aquí el cambio
    gerente_id: Optional[int] = Field(default=None, foreign_key="empleado.id")

    gerente: Optional["Empleado"] = Relationship(back_populates="proyectos")

class ProyectoCreate(SQLModel):
    nombre: str
    descripcion: str
    presupuesto: float
    estado: bool = True  # 👈 también aquí
    gerente_id: Optional[int] = None
