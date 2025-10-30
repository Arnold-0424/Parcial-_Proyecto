from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables

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

@app.get("/")
def home():
    """Ruta raíz del sistema."""
    return {"mensaje": "🚀 API de Gestión de Proyectos activa y lista para trabajar"}
