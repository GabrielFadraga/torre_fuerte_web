# TFuerte/state/solicitante_fin_state.py
import reflex as rx
from typing import List
from TFuerte.api.solicitante_auth_api import SolicitanteAuthAPI
from TFuerte.api.financiamiento_api import FinanciamientoApi
from TFuerte.routes import Route

class SolicitanteFinState(rx.State):
    """Estado para el solicitante de financiamiento"""
    
    # Autenticación (usa la misma tabla que recursos)
    current_solicitante_fin: dict = {}
    is_authenticated_fin: bool = False
    usuario_fin: str = ""
    clave_fin: str = ""
    error_message_fin: str = ""
    loading_auth_fin: bool = False
    
    # Formulario
    area_solicitante: str = ""
    fecha: str = ""
    servicio: str = ""
    numero_contrato: str = ""
    orden_trabajo: str = ""
    descripcion: str = ""
    cantidad: str = ""
    loading: bool = False
    show_success: bool = False
    
    # Lista de tipos de productos para el select
    tipos_productos: List[str] = []
    productos_por_tipo: List[dict] = []
    
    # Historial de solicitudes
    mis_solicitudes_fin: List[dict] = []
    
    # Setters básicos
    def set_area_solicitante(self, area: str):
        self.area_solicitante = area
    
    def set_fecha(self, fecha: str):
        self.fecha = fecha
    
    def set_servicio(self, servicio: str):
        self.servicio = servicio
        # Cuando cambia el tipo, cargar productos de ese tipo
        if servicio:
            self.cargar_productos_por_tipo(servicio)
    
    def set_numero_contrato(self, numero: str):
        self.numero_contrato = numero
    
    def set_orden_trabajo(self, orden: str):
        self.orden_trabajo = orden
    
    def set_descripcion(self, descripcion: str):
        self.descripcion = descripcion
    
    def set_cantidad(self, cantidad: str):
        self.cantidad = cantidad
    
    # Setters para autenticación
    def set_usuario_fin(self, usuario: str):
        self.usuario_fin = usuario
    
    def set_clave_fin(self, clave: str):
        self.clave_fin = clave
    
    # Autenticación (usa la misma API que recursos)
    def sign_in_fin(self, form_data: dict = None):
        """Inicia sesión como solicitante (misma tabla que recursos)"""
        self.loading_auth_fin = True
        
        username = form_data.get("username", "") if form_data else self.usuario_fin
        password = form_data.get("password", "") if form_data else self.clave_fin
        
        if not username or not password:
            self.error_message_fin = "Usuario y contraseña son requeridos"
            self.loading_auth_fin = False
            return rx.toast.error("❌ Usuario y contraseña son requeridos")
        
        response = SolicitanteAuthAPI.sign_in(username, password)
        
        if response.get("success"):
            self.is_authenticated_fin = True
            self.current_solicitante_fin = response.get("user", {})
            self.usuario_fin = ""
            self.clave_fin = ""
            self.error_message_fin = ""
            
            # Cargar tipos de productos
            self.cargar_tipos_productos()
            
            self.loading_auth_fin = False
            
            return rx.redirect(Route.SOLICITANTE_FIN_FORM.value)
        else:
            self.error_message_fin = response.get("error", "Error al iniciar sesión")
            self.loading_auth_fin = False
            return rx.toast.error(f"❌ {self.error_message_fin}")
    
    def cargar_tipos_productos(self):
        """Carga los tipos de productos disponibles"""
        self.tipos_productos = FinanciamientoApi.get_tipos_productos()
    
    def cargar_productos_por_tipo(self, tipo: str):
        """Carga los productos de un tipo específico"""
        self.productos_por_tipo = FinanciamientoApi.get_productos_por_tipo(tipo)
    
    def sign_out_fin(self):
        """Cierra sesión del solicitante"""
        self.is_authenticated_fin = False
        self.current_solicitante_fin = {}
        self.mis_solicitudes_fin = []
        return rx.redirect(Route.SOLICITANTEFIN_LOGIN.value)
    
    # Crear solicitud
    def crear_solicitud_fin(self, form_data: dict):
        """Crea una solicitud de financiamiento"""
        if not self.is_authenticated_fin:
            return rx.toast.error("❌ No estás autenticado")
        
        self.loading = True
        
        # Validar cantidad
        try:
            cantidad_int = int(self.cantidad)
        except:
            self.loading = False
            return rx.toast.error("❌ La cantidad debe ser un número entero")
        
        # Preparar datos
        solicitud_data = {
            "Area solicitante": self.area_solicitante,
            "Fecha": self.fecha,
            "Servicio": self.servicio,
            "Numero de contrato/suplemento": self.numero_contrato,
            "Orden de trabajo": self.orden_trabajo,
            "Descripcion": self.descripcion,
            "Cantidad": cantidad_int,
            "solicitante_id": self.current_solicitante_fin.get("id")
        }
        
        # Crear solicitud
        response = FinanciamientoApi.create_solicitud_fin(solicitud_data)
        
        if response:
            # Limpiar todo
            self.area_solicitante = ""
            self.fecha = ""
            self.servicio = ""
            self.numero_contrato = ""
            self.orden_trabajo = ""
            self.descripcion = ""
            self.cantidad = ""
            self.show_success = True
            
            # Recargar historial
            self.load_mis_solicitudes_fin()
            
            return rx.toast.success("✅ Solicitud de financiamiento creada")
        else:
            return rx.toast.error("❌ Error al crear la solicitud")
        
        self.loading = False
    
    # Cargar historial
    def load_mis_solicitudes_fin(self):
        """Carga las solicitudes de financiamiento del solicitante actual"""
        if not self.is_authenticated_fin:
            return
        
        self.loading = True
        
        solicitante_id = self.current_solicitante_fin.get("id")
        if solicitante_id:
            solicitudes_data = FinanciamientoApi.get_solicitudes_fin_by_solicitante(solicitante_id)
            self.mis_solicitudes_fin = solicitudes_data
        
        self.loading = False
    
    def close_success_dialog(self):
        """Cierra el diálogo de éxito"""
        self.show_success = False
    
    # Variables computadas
    @rx.var
    def total_solicitudes_fin(self) -> int:
        return len(self.mis_solicitudes_fin)