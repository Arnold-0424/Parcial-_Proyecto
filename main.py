from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routers import empleados, proyectos, asignaciones

  # Cambiamos el parámetro 'app' a 'app_instance'
@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    print("🟢 Iniciando aplicación y creando tablas...")
    create_db_and_tables()
    yield
    print("🔴 Cerrando aplicación...")

  # Creamos la app principal
app = FastAPI(
    title="Sistema de Gestión de Proyectos",
    description="API para la administración de empleados y proyectos.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(empleados.router)
app.include_router(proyectos.router)
app.include_router(asignaciones.router)

@app.get("/")
def home():
    """Ruta raíz del sistema."""
    return {"mensaje": "🚀 API de Gestión de Proyectos activa y lista para trabajar"}


