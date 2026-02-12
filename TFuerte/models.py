# TFuerte/models.py
from typing import List, Optional
import reflex as rx

class RecursoModel(rx.Base):
    """Modelo para un recurso individual"""
    descripcion: str = ""
    unidad_medida: str = ""
    cantidad: float = 0.0
    observaciones: str = ""

class SolicitudModel(rx.Base):
    """Modelo para una solicitud con recursos"""
    id: Optional[int] = None
    centro_costo: str = ""
    fecha: str = ""
    orden_trabajo: str = ""
    estado: str = "pendiente"
    fecha_creacion: str = ""
    fecha_creacion_display: str = ""
    num_recursos: int = 0
    recursos: List[RecursoModel] = []
    observaciones: str = ""  # AGREGAR ESTA LÍNEA