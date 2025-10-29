from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date

# Evita importaciones circulares
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.empleado import Empleado


class Proyecto(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, nullable=False, unique=True, description="Nombre único del proyecto")
    descripcion: str = Field(nullable=False, description="Descripción breve del proyecto")
    presupuesto: float = Field(gt=0, description="Presupuesto asignado al proyecto en COP")
    estado: str = Field(default="En curso", description="Estado actual del proyecto")
    fecha_inicio: date = Field(default_factory=date.today, description="Fecha de creación del proyecto")

    # Relación 1:N con Empleado (gerente)
    gerente_id: Optional[int] = Field(default=None, foreign_key="empleado.id")

    # Relaciones
    gerente: Optional["Empleado"] = Relationship(back_populates="proyectos_dirigidos")  # gerente
    empleados: List["ProyectoEmpleadoLink"] = Relationship(back_populates="proyecto")  # relación N:M

    def __repr__(self):
        return f"<Proyecto(nombre={self.nombre}, estado={self.estado}, presupuesto={self.presupuesto})>"


# Modelo para creación de proyectos
class ProyectoCreate(SQLModel):
    nombre: str
    descripcion: str
    presupuesto: float
    estado: Optional[str] = "En curso"
    gerente_id: Optional[int] = None


# Modelo para lectura de proyectos
class ProyectoRead(SQLModel):
    id: int
    nombre: str
    descripcion: str
    presupuesto: float
    estado: str
    gerente_id: Optional[int]
