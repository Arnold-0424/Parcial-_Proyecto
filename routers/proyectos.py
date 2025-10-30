from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from models.proyecto import Proyecto, ProyectoCreate
from models.empleado import Empleado
from database import get_session

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])


@router.post("/", response_model=Proyecto, status_code=status.HTTP_201_CREATED)
def crear_proyecto(data: ProyectoCreate, session: Session = Depends(get_session)):

    # Verificar que el gerente exista
    gerente = session.get(Empleado, data.gerente_id)
    if not gerente:
        raise HTTPException(status_code=404, detail="Gerente no encontrado")

    # Crear proyecto
    proyecto = Proyecto.model_validate(data)
    session.add(proyecto)
    session.commit()
    session.refresh(proyecto)
    return proyecto


@router.get("/", response_model=list[Proyecto])
def listar_proyectos(
    estado: bool | None = True,
    presupuesto_min: float | None = None,
    session: Session = Depends(get_session),):

    #Lista proyectos con opción de filtrar por estado y presupuesto mínimo.
    query = select(Proyecto)
    if estado is not None:
        query = query.where(Proyecto.estado == estado)
    if presupuesto_min is not None:
        query = query.where(Proyecto.presupuesto >= presupuesto_min)

    proyectos = session.exec(query).all()
    return proyectos


@router.get("/{proyecto_id}", response_model=Proyecto)
def obtener_proyecto(proyecto_id: int, session: Session = Depends(get_session)):

    #Obtiene la información de un proyecto, incluyendo su gerente.
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    # Verificar que el gerente esté activo
    if proyecto.gerente and not proyecto.gerente.estado:
        raise HTTPException(status_code=409, detail="El gerente asignado está inactivo")

    return proyecto


@router.put("/{proyecto_id}", response_model=Proyecto)
def actualizar_proyecto(
    proyecto_id: int, data: ProyectoCreate, session: Session = Depends(get_session)):

    #Actualiza los datos de un proyecto existente.
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    gerente = session.get(Empleado, data.gerente_id)
    if not gerente:
        raise HTTPException(status_code=404, detail="Gerente no encontrado")

    proyecto.nombre = data.nombre
    proyecto.descripcion = data.descripcion
    proyecto.presupuesto = data.presupuesto
    proyecto.estado = data.estado
    proyecto.gerente_id = data.gerente_id

    session.add(proyecto)
    session.commit()
    session.refresh(proyecto)
    return proyecto


@router.delete("/{proyecto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_proyecto(proyecto_id: int, session: Session = Depends(get_session)):

    #Eliminación lógica de un proyecto (estado = False).
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    proyecto.estado = False
    session.add(proyecto)
    session.commit()
    return {"mensaje": "Proyecto marcado como inactivo"}
