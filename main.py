from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "Sistema de Gestión de Proyectos activo ✅"}
