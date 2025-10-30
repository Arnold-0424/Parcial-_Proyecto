from fastapi import HTTPException, status
from sqlmodel import Session, select
from models.empleado import Empleado
from models.proyecto import Proyecto

#  VALIDACIONES DE EMPLEADOS
def validar_empleado_unico(session: Session, nombre: str):

    # Verifica que no exista otro empleado con el mismo nombre.
    empleado_existente = session.exec(select(Empleado).where(Empleado.nombre == nombre)).first()
    if empleado_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un empleado con el nombre '{nombre}'."
        )


def validar_salario_valido(salario: float):

    # Verifica que el salario sea mayor que cero.
    if salario <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El salario debe ser mayor que cero."
        )

# VALIDACIONES DE PROYECTOS
def validar_proyecto_unico(session: Session, nombre: str):

    # Evita que se creen proyectos con nombres repetidos
    proyecto_existente = session.exec(select(Proyecto).where(Proyecto.nombre == nombre)).first()
    if proyecto_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un proyecto con el nombre '{nombre}'."
        )


def validar_presupuesto_valido(presupuesto: float):

    #Verifica que el presupuesto sea mayor que cero.
    if presupuesto <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El presupuesto debe ser mayor que cero."
        )


def validar_gerente_activo(session: Session, gerente_id: int):

    # Valida que el gerente exista y esté activo.
    gerente = session.get(Empleado, gerente_id)
    if not gerente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El gerente no existe.")
