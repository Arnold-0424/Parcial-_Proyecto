from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from models.empleado import Empleado
from models.proyecto import Proyecto
from models.relacion import ProyectoEmpleadoLink
from database import get_session

router = APIRouter(prefix="/asignaciones", tags=["Asignaciones"])

# ---------------------------------------------------------------------
# ✅ 1. ASIGNAR EMPLEADO A PROYECTO
# ---------------------------------------------------------------------
@router.post("/empleado/{empleado_id}/proyecto/{proyecto_id}", status_code=status.HTTP_201_CREATED)
def asignar_empleado_a_proyecto(
    empleado_id: int, proyecto_id: int, session: Session = Depends(get_session)
):
    """
    ✅ Asigna un empleado a un proyecto, evitando duplicados.
    """
    empleado = session.get(Empleado, empleado_id)
    proyecto = session.get(Proyecto, proyecto_id)

    if not empleado or not proyecto:
        raise HTTPException(status_code=404, detail="Empleado o proyecto no encontrado")

    # Verificar si ya existe la asignación
    asignacion_existente = session.exec(
        select(ProyectoEmpleadoLink).where(
            ProyectoEmpleadoLink.empleado_id == empleado_id,
            ProyectoEmpleadoLink.proyecto_id == proyecto_id,
        )
    ).first()

    if asignacion_existente:
        raise HTTPException(
            status_code=400, detail="El empleado ya está asignado a este proyecto"
        )

    nueva_asignacion = ProyectoEmpleadoLink(
        empleado_id=empleado_id, proyecto_id=proyecto_id
    )
    session.add(nueva_asignacion)
    session.commit()

    return {
        "mensaje": f"Empleado con ID {empleado_id} asignado correctamente al proyecto con ID {proyecto_id}.",
        "empleado_id": empleado_id,
        "proyecto_id": proyecto_id,
        "estado": "Asignación exitosa"
    }

# ---------------------------------------------------------------------
# ✅ 2. DESASIGNAR EMPLEADO DE PROYECTO
# ---------------------------------------------------------------------
@router.delete("/empleado/{empleado_id}/proyecto/{proyecto_id}", status_code=status.HTTP_200_OK)
def desasignar_empleado_de_proyecto(
    empleado_id: int, proyecto_id: int, session: Session = Depends(get_session)
):
    """
    ✅ Elimina una asignación entre un empleado y un proyecto.
    Devuelve un mensaje de confirmación con los IDs involucrados.
    """
    asignacion = session.exec(
        select(ProyectoEmpleadoLink).where(
            (ProyectoEmpleadoLink.empleado_id == empleado_id)
            & (ProyectoEmpleadoLink.proyecto_id == proyecto_id)
        )
    ).first()

    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")

    session.delete(asignacion)
    session.commit()

    return {
        "mensaje": f"El empleado con ID {empleado_id} fue desvinculado del proyecto con ID {proyecto_id}.",
        "empleado_id": empleado_id,
        "proyecto_id": proyecto_id,
        "estado": "Desasignación completada exitosamente"
    }

# ---------------------------------------------------------------------
# ✅ 3. LISTAR PROYECTOS DE UN EMPLEADO
# ---------------------------------------------------------------------
@router.get("/empleado/{empleado_id}", response_model=list[Proyecto])
def proyectos_de_empleado(empleado_id: int, session: Session = Depends(get_session)):
    """
    ✅ Devuelve todos los proyectos en los que participa un empleado específico.
    """
    empleado = session.get(Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    proyectos = session.exec(
        select(Proyecto)
        .join(ProyectoEmpleadoLink)
        .where(ProyectoEmpleadoLink.empleado_id == empleado_id)
    ).all()

    if not proyectos:
        raise HTTPException(
            status_code=404,
            detail=f"El empleado con ID {empleado_id} no tiene proyectos asignados."
        )

    return proyectos

# ---------------------------------------------------------------------
# ✅ 4. LISTAR EMPLEADOS DE UN PROYECTO
# ---------------------------------------------------------------------
@router.get("/proyecto/{proyecto_id}", response_model=list[Empleado])
def empleados_de_proyecto(proyecto_id: int, session: Session = Depends(get_session)):
    """
    ✅ Lista todos los empleados asignados a un proyecto específico.
    """
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    empleados = session.exec(
        select(Empleado)
        .join(ProyectoEmpleadoLink)
        .where(ProyectoEmpleadoLink.proyecto_id == proyecto_id)
    ).all()

    if not empleados:
        raise HTTPException(
            status_code=404,
            detail=f"No hay empleados asignados al proyecto con ID {proyecto_id}"
        )

    return empleados
