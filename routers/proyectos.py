from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from models.proyecto import Proyecto, ProyectoCreate
from models.empleado import Empleado
from database import get_session

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])


# Crear proyecto (con validación de nombre único)
@router.post("/", response_model=Proyecto, status_code=status.HTTP_201_CREATED)
def crear_proyecto(data: ProyectoCreate, session: Session = Depends(get_session)):
    """
    Crea un nuevo proyecto con un gerente asignado, validando que:
    - El gerente exista.
    - El nombre del proyecto no esté repetido.
    """
    # Verificar que el gerente exista
    gerente = session.get(Empleado, data.gerente_id)
    if not gerente:
        raise HTTPException(status_code=404, detail="Gerente no encontrado")

    # Verificar nombre de proyecto duplicado
    proyecto_existente = session.exec(
        select(Proyecto).where(Proyecto.nombre == data.nombre)
    ).first()

    if proyecto_existente:
        raise HTTPException(
            status_code=409, detail="Ya existe un proyecto con ese nombre"
        )

    # Crear proyecto nuevo
    proyecto = Proyecto.model_validate(data)
    session.add(proyecto)
    session.commit()
    session.refresh(proyecto)
    return proyecto


# Listar proyectos (con filtros)
@router.get("/", response_model=list[Proyecto])
def listar_proyectos(
    estado: bool | None = True,
    presupuesto_min: float | None = None,
    session: Session = Depends(get_session),
):
    """
    Lista los proyectos existentes.
    Permite filtrar por estado (activo/inactivo) y presupuesto mínimo.
    """
    query = select(Proyecto)
    if estado is not None:
        query = query.where(Proyecto.estado == estado)
    if presupuesto_min is not None:
        query = query.where(Proyecto.presupuesto >= presupuesto_min)

    proyectos = session.exec(query).all()
    return proyectos


# Obtener proyecto (incluye gerente)
@router.get("/{proyecto_id}", response_model=Proyecto)
def obtener_proyecto(proyecto_id: int, session: Session = Depends(get_session)):
    """
    Obtiene la información detallada de un proyecto,
    incluyendo su gerente asignado.
    """
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    if proyecto.gerente and not proyecto.gerente.estado:
        raise HTTPException(status_code=409, detail="El gerente está inactivo")

    return proyecto


# Actualizar proyecto (con validación de nombre repetido)
@router.put("/{proyecto_id}", response_model=Proyecto)
def actualizar_proyecto(
    proyecto_id: int, data: ProyectoCreate, session: Session = Depends(get_session)
):
    """
    Actualiza los datos de un proyecto.
    Verifica que el nuevo nombre no esté duplicado.
    """
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    # Verificar que no exista otro proyecto con el mismo nombre
    duplicado = session.exec(
        select(Proyecto)
        .where(Proyecto.nombre == data.nombre)
        .where(Proyecto.id != proyecto_id)
    ).first()

    if duplicado:
        raise HTTPException(
            status_code=409, detail="Ya existe otro proyecto con ese nombre"
        )

    # Validar gerente
    gerente = session.get(Empleado, data.gerente_id)
    if not gerente:
        raise HTTPException(status_code=404, detail="Gerente no encontrado")

    # Actualizar campos
    proyecto.nombre = data.nombre
    proyecto.descripcion = data.descripcion
    proyecto.presupuesto = data.presupuesto
    proyecto.estado = data.estado
    proyecto.gerente_id = data.gerente_id

    session.add(proyecto)
    session.commit()
    session.refresh(proyecto)
    return proyecto


# Eliminación lógica del proyecto
@router.delete("/{proyecto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_proyecto(proyecto_id: int, session: Session = Depends(get_session)):
    """
    Marca un proyecto como inactivo en lugar de eliminarlo físicamente.
    """
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    proyecto.estado = False
    session.add(proyecto)
    session.commit()
    return {"mensaje": "Proyecto marcado como inactivo"}
