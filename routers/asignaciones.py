from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from models.empleado import Empleado
from models.proyecto import Proyecto
from models.relacion import ProyectoEmpleadoLink
from database import get_session

router = APIRouter(prefix="/asignaciones", tags=["Asignaciones"])

#  Asignar empleado a proyecto
@router.post("/", status_code=status.HTTP_201_CREATED)
def asignar_empleado(proyecto_id: int, empleado_id: int, session: Session = Depends(get_session)):

    # Asigna un empleado a un proyecto, evitando duplicaciones.

    proyecto = session.get(Proyecto, proyecto_id)
    empleado = session.get(Empleado, empleado_id)

    if not proyecto or not empleado:
        raise HTTPException(status_code=404, detail="Proyecto o empleado no encontrado")

    # Verificar duplicado
    existe = session.exec(
        select(ProyectoEmpleadoLink).where(
            ProyectoEmpleadoLink.proyecto_id == proyecto_id,
            ProyectoEmpleadoLink.empleado_id == empleado_id
        )
    ).first()

    if existe:
        raise HTTPException(status_code=409, detail="El empleado ya está asignado a este proyecto")

    link = ProyectoEmpleadoLink(proyecto_id=proyecto_id, empleado_id=empleado_id)
    session.add(link)
    session.commit()
    return {"mensaje": f"Empleado {empleado.nombre} asignado al proyecto {proyecto.nombre}"}


#  Desasignar empleado de proyecto
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def desasignar_empleado(proyecto_id: int, empleado_id: int, session: Session = Depends(get_session)):

    # Elimina la asignación de un empleado a un proyecto.
    link = session.exec(
        select(ProyectoEmpleadoLink).where(
            ProyectoEmpleadoLink.proyecto_id == proyecto_id,
            ProyectoEmpleadoLink.empleado_id == empleado_id
        )
    ).first()

    if not link:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")

    session.delete(link)
    session.commit()
    return {"mensaje": "Empleado desasignado correctamente"}


# Proyectos de un empleado
@router.get("/empleado/{empleado_id}")
def proyectos_de_empleado(empleado_id: int, session: Session = Depends(get_session)):

    # Obtiene todos los proyectos en los que trabaja un empleado.
    empleado = session.get(Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    proyectos = session.exec(
        select(Proyecto).join(ProyectoEmpleadoLink).where(ProyectoEmpleadoLink.empleado_id == empleado_id)
    ).all()

    return {"empleado": empleado.nombre, "proyectos": proyectos}


#  Empleados de un proyecto
@router.get("/proyecto/{proyecto_id}")
def empleados_de_proyecto(proyecto_id: int, session: Session = Depends(get_session)):

    # Obtiene todos los empleados asignados a un proyecto
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    empleados = session.exec(
        select(Empleado).join(ProyectoEmpleadoLink).where(ProyectoEmpleadoLink.proyecto_id == proyecto_id)
    ).all()

    return {"proyecto": proyecto.nombre, "empleados": empleados}

# Obtener proyecto con gerente y empleados
@router.get("/detalle/{proyecto_id}")
def detalle_proyecto(proyecto_id: int, session: Session = Depends(get_session)):

    # Devuelve la información completa de un proyecto, su gerente y sus empleados.
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    gerente = session.get(Empleado, proyecto.gerente_id) if proyecto.gerente_id else None
    empleados = session.exec(
        select(Empleado).join(ProyectoEmpleadoLink).where(ProyectoEmpleadoLink.proyecto_id == proyecto_id)
    ).all()

    return {
        "proyecto": proyecto.nombre,
        "descripcion": proyecto.descripcion,
        "presupuesto": proyecto.presupuesto,
        "estado": proyecto.estado,
        "gerente": gerente.nombre if gerente else None,
        "empleados": [e.nombre for e in empleados],
    }
