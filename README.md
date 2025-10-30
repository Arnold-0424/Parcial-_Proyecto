# 🧩 Sistema de Gestión de Empleados y Proyectos – FastAPI

Proyecto desarrollado con **FastAPI + SQLModel**, que permite gestionar empleados, proyectos y sus asignaciones.  
Incluye validaciones, relaciones N:M, y documentación automática con Swagger UI.

---

## 🚀 Funcionalidades principales

### 👷 Empleados
- Registrar empleados con **nombre**, **especialidad** y **salario**.  
- Consultar empleados activos o filtrados por especialidad.  
- Buscar empleado por nombre.  
- Actualizar datos de un empleado existente.  
- Desactivar empleados (*borrado lógico* con confirmación).

### 🧱 Proyectos
- Registrar nuevos proyectos con **nombre**, **descripción**, **presupuesto** y **gerente asignado**.  
- Listar proyectos activos o inactivos.  
- Actualizar información del proyecto.  
- Marcar proyecto como inactivo (*borrado lógico*).  

### 🔗 Asignaciones (Empleado ↔ Proyecto)
- Asignar empleados a proyectos (**relación N:M**).  
- Consultar todos los empleados que participan en un proyecto.  
- Consultar todos los proyectos en los que participa un empleado.  
- Desasignar empleados de proyectos con mensaje informativo.

---

## 🧰 Tecnologías utilizadas

- 🐍 **Python 3.13**  
- ⚡ **FastAPI** (API moderna y de alto rendimiento)  
- 🗃️ **SQLModel** (ORM + tipado con Pydantic)  
- 🔥 **Uvicorn** (servidor ASGI)  
- 🧱 **SQLite** (base de datos local)  
- 🧩 **Pydantic** (validaciones y modelos de datos)

---

## ⚙️ Estructura del proyecto

```bash
Parcial_Proyecto/
│
├── main.py                     # Punto de entrada principal
├── database.py                 # Conexión y creación de tablas
│
├── models/                     # Modelos SQLModel
│   ├── empleado.py             # Modelo de empleados
│   ├── proyecto.py             # Modelo de proyectos
│   └── relacion.py             # Relación N:M entre ambos
│
├── routers/                    # Rutas organizadas por entidad
│   ├── empleados.py            # Endpoints para empleados
│   ├── proyectos.py            # Endpoints para proyectos
│   └── asignaciones.py         # Endpoints para asignaciones
│
└── utils/
    └── validaciones.py         # Validaciones personalizadas


---


## 📡 Endpoints principales

### 👨‍💼 Empleados

| Método     | Endpoint                     | Descripción                                         |
|:----------:|:----------------------------:|:----------------------------------------------------|
| **POST**   | `/empleados/`                | Crear empleado                                      |
| **GET**    | `/empleados/`                | Listar empleados activos o filtrar por especialidad |
| **GET**    | `/empleados/buscar/{nombre}` | Buscar empleado por nombre                          |
| **PUT**    | `/empleados/{empleado_id}`   | Actualizar empleado                                 |
| **DELETE** | `/empleados/{empleado_id}`   | Marcar empleado como inactivo                       |

---

### 🏗️ Proyectos

| Método | Endpoint | Descripción |
|:--------:|:-----------:|:-------------|
| **POST** | `/proyectos/` | Crear proyecto |
| **GET** | `/proyectos/` | Listar proyectos activos |
| **GET** | `/proyectos/{proyecto_id}` | Consultar proyecto específico |
| **PUT** | `/proyectos/{proyecto_id}` | Actualizar información |
| **DELETE** | `/proyectos/{proyecto_id}` | Marcar proyecto como inactivo |

---

### 🔗 Asignaciones

| Método | Endpoint | Descripción |
|:--------:|:-----------:|:-------------|
| **POST** | `/asignaciones/empleado/{empleado_id}/proyecto/{proyecto_id}` | Asignar empleado a proyecto |
| **GET** | `/asignaciones/proyecto/{proyecto_id}` | Ver empleados de un proyecto |
| **GET** | `/asignaciones/empleado/{empleado_id}` | Ver proyectos de un empleado |
| **DELETE** | `/asignaciones/empleado/{empleado_id}/proyecto/{proyecto_id}` | Desasignar empleado de proyecto |

---

git clone https://github.com/tuusuario/gestion_proyectos_fastapi.git
cd gestion_proyectos_fastapi

