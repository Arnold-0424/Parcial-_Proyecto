from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from models.proyecto import Proyecto, ProyectoCreate
from models.empleado import Empleado
from models.relacion import ProyectoEmpleadoLink
from database import get_session

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])



#  CREAR PROYECTO
@router.post("/", response_model=Proyecto, status_code=status.HTTP_201_CREATED)
def crear_proyecto(data: ProyectoCreate, session: Session = Depends(get_session)):

    # Crea un nuevo proyecto, validando que el gerente exista.
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

# ISTAR PROYECTOS (con filtros simples)

@router.get("/", response_model=List[Proyecto])
def listar_proyectos(
    estado: Optional[bool] = Query(None, description="Filtra por estado del proyecto"),
    presupuesto_min: Optional[float] = Query(None, description="Presupuesto mínimo"),
    presupuesto_max: Optional[float] = Query(None, description="Presupuesto máximo"),
    session: Session = Depends(get_session),
):

    # Lista proyectos filtrando por estado y rango de presupuesto.
    query = select(Proyecto)
    if estado is not None:
        query = query.where(Proyecto.estado == estado)
    if presupuesto_min is not None:
        query = query.where(Proyecto.presupuesto >= presupuesto_min)
    if presupuesto_max is not None:
        query = query.where(Proyecto.presupuesto <= presupuesto_max)

    proyectos = session.exec(query).all()
    return proyectos


#  OBTENER PROYECTO POR ID
@router.get("/{proyecto_id}", response_model=Proyecto)
def obtener_proyecto(proyecto_id: int, session: Session = Depends(get_session)):

    # Obtiene la información de un proyecto, incluyendo su gerente.
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    # Verificar que el gerente esté activo
    if proyecto.gerente and not proyecto.gerente.estado:
        raise HTTPException(status_code=409, detail="El gerente asignado está inactivo")

    return proyecto


#  ACTUALIZAR PROYECTO

@router.put("/{proyecto_id}", response_model=Proyecto)
def actualizar_proyecto(
    proyecto_id: int, data: ProyectoCreate, session: Session = Depends(get_session)
):

    # Actualiza los datos de un proyecto existente
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



# 🗑ELIMINAR PROYECTO (lógico)
@router.delete("/{proyecto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_proyecto(proyecto_id: int, session: Session = Depends(get_session)):

    # Eliminación lógica de un proyecto (estado = False)
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    proyecto.estado = False
    session.add(proyecto)
    session.commit()
    return {"mensaje": "Proyecto marcado como inactivo"}



# CONSULTAS CRUZADAS Y FILTROS AVANZADOS
@router.get("/detalle/{proyecto_id}")
def obtener_proyecto_detallado(proyecto_id: int, session: Session = Depends(get_session)):

    # Devuelve un proyecto con su gerente y los empleados asignados.
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    gerente = session.get(Empleado, proyecto.gerente_id) if proyecto.gerente_id else None

    empleados = (
        session.exec(
            select(Empleado)
            .join(ProyectoEmpleadoLink)
            .where(ProyectoEmpleadoLink.proyecto_id == proyecto_id)
        ).all()
    )

    return {
        "proyecto": proyecto,
        "gerente": gerente,
        "empleados_asignados": empleados,
    }


@router.get("/activos/detalle")
def listar_proyectos_activos_con_empleados(session: Session = Depends(get_session)):

    # Lista todos los proyectos activos con su gerente y empleados asignados.
    proyectos_activos = session.exec(select(Proyecto).where(Proyecto.estado == True)).all()

    resultado = []
    for proyecto in proyectos_activos:
        gerente = session.get(Empleado, proyecto.gerente_id) if proyecto.gerente_id else None
        empleados = (
            session.exec(
                select(Empleado)
                .join(ProyectoEmpleadoLink)
                .where(ProyectoEmpleadoLink.proyecto_id == proyecto.id)
            ).all()
        )
        resultado.append(
            {
                "proyecto": proyecto,
                "gerente": gerente,
                "empleados": empleados,
            }
        )
    return resultado
