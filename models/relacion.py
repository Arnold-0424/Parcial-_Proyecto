from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.empleado import Empleado
    from models.proyecto import Proyecto

class ProyectoEmpleadoLink(SQLModel, table=True):

    #Relación N:M entre Empleado y Proyecto.

    empleado_id: int = Field(foreign_key="empleado.id", primary_key=True)
    proyecto_id: int = Field(foreign_key="proyecto.id", primary_key=True)

    # Relaciones inversas
    empleado: Optional["Empleado"] = Relationship(back_populates="proyectos")
    proyecto: Optional["Proyecto"] = Relationship(back_populates="empleados")