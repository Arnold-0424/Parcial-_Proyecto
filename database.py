from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# 🔹 echo=True = muestra las consultas SQL en consola
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    """Crea las tablas en la base de datos."""
    from models.empleado import Empleado  # noqa: F401
    from models.proyecto import Proyecto  # noqa: F401
    from models.relacion import ProyectoEmpleadoLink  # noqa: F401
    SQLModel.metadata.create_all(engine)

def get_session():
    """Proporciona una sesión de base de datos"""
    with Session(engine) as session:
        yield session
