from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from models.proyecto import ProyectoCreate, Proyecto
from models.empleado import Empleado
from database import get_session
from utils.validaciones import (
    validar_proyecto_unico,
    validar_presupuesto_valido,
    validar_gerente_activo)

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])


#  CREAR PROYECTO
@router.post("/", response_model=Proyecto)
def crear_proyecto(data: ProyectoCreate, session: Session = Depends(get_session)):
    validar_proyecto_unico(session, data.nombre)
    validar_presupuesto_valido(data.presupuesto)

    if data.gerente_id:
        validar_gerente_activo(session, data.gerente_id)

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


# ✅ Buscar proyecto por nombre
@router.get("/buscar/{nombre}", response_model=Proyecto)
def buscar_proyecto_por_nombre(nombre: str, session: Session = Depends(get_session)):
    proyecto = session.exec(select(Proyecto).where(Proyecto.nombre == nombre)).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail=f"Proyecto '{nombre}' no encontrado")
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



@router.delete("/{proyecto_id}", status_code=status.HTTP_200_OK)
def eliminar_proyecto(proyecto_id: int, session: Session = Depends(get_session)):
    """
    Elimina lógicamente un proyecto (marca su estado como inactivo).
    """
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    # Marcar el proyecto como inactivo
    proyecto.estado = False
    session.add(proyecto)
    session.commit()

    # ✅ Mensaje de confirmación visible en Swagger
    return {
        "mensaje": f"Proyecto '{proyecto.nombre}' marcado como inactivo.",
        "id": proyecto.id,
        "estado": proyecto.estado
    }


