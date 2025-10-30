from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from database import get_session
from models.empleado import Empleado, EmpleadoCreate
from utils.validaciones import validar_empleado_unico, validar_salario_valido

router = APIRouter(prefix="/empleados", tags=["Empleados"])


# ✅ Crear empleado
@router.post("/", response_model=Empleado, status_code=status.HTTP_201_CREATED)
def crear_empleado(data: EmpleadoCreate, session: Session = Depends(get_session)):
    validar_empleado_unico(session, data.nombre)
    validar_salario_valido(data.salario)

    empleado = Empleado.model_validate(data)
    session.add(empleado)
    session.commit()
    session.refresh(empleado)
    return empleado


# ✅ Listar empleados (con filtros opcionales)
@router.get("/", response_model=list[Empleado])
def listar_empleados(
    especialidad: str | None = None,
    activo: bool | None = True,
    session: Session = Depends(get_session)
):
    """
    Lista empleados, con opción de filtrar por especialidad o estado activo.
    """
    query = select(Empleado)
    if especialidad:
        query = query.where(Empleado.especialidad == especialidad)
    if activo is not None:
        query = query.where(Empleado.estado == activo)

    empleados = session.exec(query).all()
    return empleados


# ✅ Buscar empleado por nombre
@router.get("/buscar/{nombre}", response_model=Empleado)
def buscar_empleado_por_nombre(nombre: str, session: Session = Depends(get_session)):
    empleado = session.exec(select(Empleado).where(Empleado.nombre == nombre)).first()
    if not empleado:
        raise HTTPException(status_code=404, detail=f"Empleado '{nombre}' no encontrado")
    return empleado


# ✅ Actualizar empleado por ID
@router.put("/{empleado_id}", response_model=Empleado)
def actualizar_empleado(
    empleado_id: int,
    data: EmpleadoCreate,
    session: Session = Depends(get_session)
):
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


# ✅ Eliminación lógica (borrado lógico)
@router.delete("/{empleado_id}", status_code=status.HTTP_200_OK)
def eliminar_empleado(empleado_id: int, session: Session = Depends(get_session)):
    """
    Elimina lógicamente un empleado (marca su estado como inactivo).
    """
    empleado = session.get(Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    # Marcar el empleado como inactivo
    empleado.estado = False
    session.add(empleado)
    session.commit()

    # ✅ Devolvemos un mensaje para confirmar
    return {
        "mensaje": f"Empleado '{empleado.nombre}' marcado como inactivo.",
        "id": empleado.id,
        "estado": empleado.estado
    }
