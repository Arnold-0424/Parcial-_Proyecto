from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from models.empleado import Empleado, EmpleadoCreate
from database import get_session
from utils.validaciones import validar_empleado_unico, validar_salario_valido

router = APIRouter(prefix="/empleados", tags=["Empleados"])


@router.post("/", response_model=Empleado)
def crear_empleado(data: EmpleadoCreate, session: Session = Depends(get_session)):
    validar_empleado_unico(session, data.nombre)
    validar_salario_valido(data.salario)

    empleado = Empleado.model_validate(data)
    session.add(empleado)
    session.commit()
    session.refresh(empleado)
    return empleado


@router.get("/", response_model=list[Empleado])
def listar_empleados(
    especialidad: str | None = None,
    activo: bool | None = True,
    session: Session = Depends(get_session)):

    #Lista empleados, con opción de filtrar por especialidad o estado activo.
    query = select(Empleado)
    if especialidad:
        query = query.where(Empleado.especialidad == especialidad)
    if activo is not None:
        query = query.where(Empleado.estado == activo)

    empleados = session.exec(query).all()
    return empleados


@router.get("/{empleado_id}", response_model=Empleado)
def obtener_empleado(empleado_id: int, session: Session = Depends(get_session)):

    # Devuelve un empleado por su ID.
    empleado = session.get(Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado


@router.put("/{empleado_id}", response_model=Empleado)
def actualizar_empleado(
    empleado_id: int, data: EmpleadoCreate, session: Session = Depends(get_session)):

    # Actualiza la información de un empleado.
    empleado = session.get(Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    empleado.nombre = data.nombre
    empleado.especialidad = data.especialidad
    empleado.salario = data.salario

    session.add(empleado)
    session.commit()
    session.refresh(empleado)
    return empleado


@router.delete("/{empleado_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_empleado(empleado_id: int, session: Session = Depends(get_session)):

    # Eliminación lógica: marca el empleado como inactivo.
    empleado = session.get(Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    empleado.estado = False
    session.add(empleado)
    session.commit()
    return {"mensaje": "Empleado marcado como inactivo"}
