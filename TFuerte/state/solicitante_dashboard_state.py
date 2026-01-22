import reflex as rx
from typing import List
from TFuerte.api.solicitudes_api import SolicitudesAPI
from datetime import datetime

class SolicitanteDashboardState(rx.State):
    """Estado para el dashboard de solicitantes"""
    
    # Formulario de nueva solicitud
    descripcion: str = ""
    cantidad: str = ""
    observacion: str = ""
    destino: str = ""
    
    # Mis solicitudes
    mis_solicitudes: List[dict] = []
    
    # ID del solicitante (se establecerá después del login)
    solicitante_id: int = 0
    solicitante_custom_id: int = 0
    
    # Estados de UI
    loading: bool = False
    
    # Computed vars para estadísticas
    @rx.var
    def computed_total_solicitudes(self) -> int:
        return len(self.mis_solicitudes)
    
    @rx.var
    def computed_pendientes(self) -> int:
        if not self.mis_solicitudes:
            return 0
        return sum(1 for s in self.mis_solicitudes if s.get("estado") == "pendiente")
    
    @rx.var
    def computed_aprobadas(self) -> int:
        if not self.mis_solicitudes:
            return 0
        return sum(1 for s in self.mis_solicitudes if s.get("estado") == "aprobada")
    
    @rx.var
    def computed_rechazadas(self) -> int:
        if not self.mis_solicitudes:
            return 0
        return sum(1 for s in self.mis_solicitudes if s.get("estado") == "rechazada")
    
    def on_load(self):
        """Se ejecuta al cargar la página"""
        print("🔄 on_load: Cargando dashboard...")
        # En Reflex, on_load puede retornar el handler directamente
        return SolicitanteDashboardState.load_mis_solicitudes
    
    @rx.event
    def load_mis_solicitudes(self):
        """Carga las solicitudes del solicitante actual"""
        self.loading = True
        yield
        
        try:
            # Verificar si tenemos el custom_id
            if not self.solicitante_custom_id:
                print("⚠️ No hay custom_id disponible")
                self.mis_solicitudes = []
                self.loading = False
                return
            
            print(f"🔍 Cargando solicitudes para custom_id: {self.solicitante_custom_id}")
            
            # Obtener solicitudes
            solicitudes = SolicitudesAPI.get_solicitudes_by_solicitante(self.solicitante_custom_id)
            
            if solicitudes:
                self.mis_solicitudes = solicitudes
                print(f"✅ {len(solicitudes)} solicitudes cargadas")
            else:
                self.mis_solicitudes = []
                print("ℹ️ No se encontraron solicitudes")
            
        except Exception as e:
            print(f"❌ Error cargando solicitudes: {e}")
            import traceback
            traceback.print_exc()
            self.mis_solicitudes = []
        
        self.loading = False
    
    def set_descripcion(self, descripcion: str):
        self.descripcion = descripcion
    
    def set_cantidad(self, cantidad: str):
        self.cantidad = cantidad
    
    def set_observacion(self, observacion: str):
        self.observacion = observacion
    
    def set_destino(self, destino: str):
        self.destino = destino
    
    @rx.event
    def set_solicitante_info(self, solicitante_info: dict):
        """Establece la información del solicitante después del login"""
        self.solicitante_id = solicitante_info.get("id", 0)
        self.solicitante_custom_id = solicitante_info.get("id_custom", 0)
        print(f"✅ Información del solicitante establecida: ID={self.solicitante_id}, CustomID={self.solicitante_custom_id}")
    
    @rx.event
    def crear_solicitud(self, form_data: dict = None):
        """Crea una nueva solicitud"""
        print("📝 Creando nueva solicitud...")
        
        # Validaciones
        if not self.descripcion.strip() or not self.cantidad.strip() or not self.destino.strip():
            yield rx.toast.error(
                "❌ Campos requeridos faltantes",
                position="top-right",
                duration=4000
            )
            return  # Importante: retornar después del yield
        
        try:
            cantidad_int = int(self.cantidad.strip())
            if cantidad_int <= 0:
                raise ValueError
        except (ValueError, TypeError):
            yield rx.toast.error(
                "❌ Cantidad inválida",
                position="top-right",
                duration=4000
            )
            return  # Importante: retornar después del yield
        
        # Verificar si tenemos el custom_id
        if not self.solicitante_custom_id or not self.solicitante_id:
            yield rx.toast.error(
                "❌ No hay sesión activa. Por favor, inicia sesión nuevamente.",
                position="top-right",
                duration=4000
            )
            return  # Importante: retornar después del yield
        
        self.loading = True
        yield  # Enviar update con loading=True
        
        try:
            # Crear la solicitud
            solicitud_data = {
                "Descripcion": self.descripcion.strip(),
                "Cantidad": cantidad_int,
                "Observacion": self.observacion.strip() or None,
                "Destino": self.destino.strip(),
                "solicitante_id": self.solicitante_id,
                "custom": self.solicitante_custom_id,
                "estado": "pendiente",
                "fecha_solicitud": datetime.now().isoformat()
            }
            
            print(f"📝 Enviando solicitud: {solicitud_data}")
            
            # Llamar a la API
            result = SolicitudesAPI.create_solicitud(solicitud_data)
            
            if result:
                # Limpiar formulario
                self.descripcion = ""
                self.cantidad = ""
                self.observacion = ""
                self.destino = ""
                
                yield rx.toast.success(
                    "✅ Solicitud creada correctamente",
                    position="top-right",
                    duration=4000
                )
                
                # Recargar solicitudes
                yield self.load_mis_solicitudes()
            else:
                yield rx.toast.error(
                    "❌ Error al crear la solicitud",
                    position="top-right",
                    duration=4000
                )
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            yield rx.toast.error(
                "❌ Error interno",
                position="top-right",
                duration=4000
            )
        
        self.loading = False
        # No se necesita yield aquí, el método finaliza naturalmente