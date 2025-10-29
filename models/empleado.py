from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from models.relacion import ProyectoEmpleadoLink

class Empleado(SQLModel, table=True):
    """
    Representa un empleado dentro del sistema de gestión de proyectos.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, nullable=False, description="Nombre completo del empleado")
    especialidad: str = Field(nullable=False, description="Área de especialización del empleado")
    salario: float = Field(gt=0, description="Salario mensual en pesos colombianos")
    estado: bool = Field(default=True, description="Activo o inactivo dentro de la empresa")

    # Relaciones (se definirán más adelante)
    proyectos: List["ProyectoEmpleadoLink"] = Relationship(back_populates="empleado")  # Relación N:M

    def __repr__(self):
        return f"<Empleado(nombre={self.nombre}, especialidad={self.especialidad}, salario={self.salario})>"


# Modelo para crear empleados (entrada de datos)
class EmpleadoCreate(SQLModel):
    nombre: str
    especialidad: str
    salario: float


# Modelo para lectura de empleados (respuesta de API)
class EmpleadoRead(SQLModel):
    id: int
    nombre: str
    especialidad: str
    salario: float
    estado: bool
