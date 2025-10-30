from fastapi import HTTPException, status


class ManejoErrores:

    # Clase centralizada para lanzar errores

    #  400 - Solicitud incorrecta
    @staticmethod
    def bad_request(mensaje: str = "Solicitud inválida"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": mensaje, "codigo": 400}
        )

    #  404 - No encontrado
    @staticmethod
    def not_found(mensaje: str = "Recurso no encontrado"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": mensaje, "codigo": 404}
        )

    #  409 - Conflicto
    @staticmethod
    def conflict(mensaje: str = "Conflicto con el estado actual del recurso"):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": mensaje, "codigo": 409}
        )

    #  201 - Creado
    @staticmethod
    def created(mensaje: str = "Recurso creado exitosamente"):
        return {"mensaje": mensaje, "codigo": 201}

    #  200 - OK
    @staticmethod
    def ok(mensaje: str = "Operación exitosa"):
        return {"mensaje": mensaje, "codigo": 200}
