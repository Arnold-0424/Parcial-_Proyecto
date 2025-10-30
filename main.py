from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routers import empleados, proyectos, asignaciones


# ✅ Configurar evento lifespan (inicio y cierre)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🟢 Iniciando aplicación y creando tablas...")
    create_db_and_tables()
    yield
    print("🔴 Cerrando aplicación...")


# ✅ Crear aplicación principal
app = FastAPI(
    title="Sistema de Gestión de Proyectos",
    description="API para la administración de empleados y proyectos.",
    version="1.0.0",
    lifespan=lifespan
)

# ✅ Incluir routers
app.include_router(empleados.router)
app.include_router(proyectos.router)
app.include_router(asignaciones.router)


# ✅ Endpoint raíz de prueba
@app.get("/")
def home():
    return {"mensaje": "🚀 API de Gestión de Proyectos activa y lista para trabajar"}
