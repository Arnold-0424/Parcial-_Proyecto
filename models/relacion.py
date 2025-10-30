from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.empleado import Empleado
    from models.proyecto import Proyecto

class ProyectoEmpleadoLink(SQLModel, table=True):
    """
    Tabla intermedia para la relación N:M entre empleados y proyectos.
    """
    empleado_id: int = Field(foreign_key="empleado.id", primary_key=True)
    proyecto_id: int = Field(foreign_key="proyecto.id", primary_key=True)

    # Relaciones inversas
    empleado: Optional["Empleado"] = Relationship(back_populates="proyectos_link")
    proyecto: Optional["Proyecto"] = Relationship(back_populates="empleados_link")
