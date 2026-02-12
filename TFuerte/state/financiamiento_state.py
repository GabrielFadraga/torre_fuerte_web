# TFuerte/state/financiamiento_state.py
import reflex as rx
from typing import List
from TFuerte.api.financiamiento_api import FinanciamientoApi
from TFuerte.api.revfin_auth_api import RevFinAuthAPI
from TFuerte.routes import Route

class FinanciamientoState(rx.State):
    """Estado para las solicitudes de financiamiento"""
    
    # Datos para RevFin
    solicitudes_pendientes_revfin: List[dict] = []
    
    # Estados de UI para RevFin
    loading_revfin: bool = False
    show_aprobar_dialog_revfin: bool = False
    show_rechazar_dialog_revfin: bool = False
    selected_solicitud_revfin: dict = {}
    search_value_revfin: str = ""
    motivo_rechazo_revfin: str = ""
    
    # Usuario actual de RevFin
    current_revfin: dict = {}
    is_authenticated_revfin: bool = False
    
    # Credenciales para login de RevFin
    username_revfin: str = ""
    password_revfin: str = ""
    error_message_revfin: str = ""
    
    # Setters para RevFin
    def set_username_revfin(self, username: str):
        self.username_revfin = username
    
    def set_password_revfin(self, password: str):
        self.password_revfin = password
    
    def set_motivo_rechazo_revfin(self, motivo: str):
        self.motivo_rechazo_revfin = motivo
    
    # Métodos de autenticación para RevFin
    @rx.event
    def sign_in_revfin(self):
        """Inicia sesión como Revisor Financiero"""
        self.loading_revfin = True
        self.error_message_revfin = ""
        yield
        
        if not self.username_revfin or not self.password_revfin:
            self.error_message_revfin = "Usuario y contraseña son requeridos"
            self.loading_revfin = False
            return
        
        response = RevFinAuthAPI.sign_in(self.username_revfin, self.password_revfin)
        
        if response["success"]:
            self.is_authenticated_revfin = True
            self.current_revfin = response["user"]
            
            self.username_revfin = ""
            self.password_revfin = ""
            
            yield rx.toast.success(
                "✅ Inicio de sesión exitoso",
                position="top-right",
                duration=3000
            )
            
            yield rx.redirect(Route.REVFIN_DASHBOARD.value)
        else:
            self.error_message_revfin = response["error"] or "Error al iniciar sesión"
            yield rx.toast.error(
                self.error_message_revfin,
                position="top-right",
                duration=4000
            )
        
        self.loading_revfin = False
    
    # Cargar datos para RevFin
    @rx.event
    def load_data_revfin(self):
        """Carga las solicitudes pendientes para revisión financiera"""
        self.loading_revfin = True
        yield
        
        solicitudes_pendientes = FinanciamientoApi.get_solicitudes_fin_pendientes_revfin()
        
        # Formatear fechas
        solicitudes_procesadas = []
        for solicitud in solicitudes_pendientes:
            solicitud_procesada = solicitud.copy()
            
            if "fecha_creacion" in solicitud_procesada and solicitud_procesada["fecha_creacion"]:
                fecha = solicitud_procesada["fecha_creacion"]
                if isinstance(fecha, str) and len(fecha) >= 10:
                    solicitud_procesada["fecha_creacion"] = fecha[:10]
            
            if "Fecha" in solicitud_procesada and solicitud_procesada["Fecha"]:
                fecha = solicitud_procesada["Fecha"]
                if isinstance(fecha, str) and len(fecha) >= 10:
                    solicitud_procesada["Fecha"] = fecha[:10]
            
            solicitudes_procesadas.append(solicitud_procesada)
        
        self.solicitudes_pendientes_revfin = solicitudes_procesadas
        self.loading_revfin = False
    
    # Filtrar solicitudes para RevFin
    def filter_solicitudes_revfin(self, search_value: str):
        """Filtra las solicitudes por término de búsqueda"""
        self.search_value_revfin = search_value
        
        if not search_value:
            return self.load_data_revfin()
        
        search_term = search_value.lower()
        filtered = []
        for s in self.solicitudes_pendientes_revfin:
            if (search_term in s.get("Descripcion", "").lower() or
                search_term in s.get("Area solicitante", "").lower() or
                search_term in s.get("Orden de trabajo", "").lower() or
                search_term in s.get("Servicio", "").lower()):
                filtered.append(s)
        
        self.solicitudes_pendientes_revfin = filtered
    
    # Diálogos para RevFin
    def open_aprobar_dialog_revfin(self, solicitud: dict):
        self.selected_solicitud_revfin = solicitud
        self.show_aprobar_dialog_revfin = True
    
    def close_aprobar_dialog_revfin(self):
        self.show_aprobar_dialog_revfin = False
        self.selected_solicitud_revfin = {}
    
    def open_rechazar_dialog_revfin(self, solicitud: dict):
        self.selected_solicitud_revfin = solicitud
        self.show_rechazar_dialog_revfin = True
        self.motivo_rechazo_revfin = ""
    
    def close_rechazar_dialog_revfin(self):
        self.show_rechazar_dialog_revfin = False
        self.selected_solicitud_revfin = {}
        self.motivo_rechazo_revfin = ""
    
    def set_show_aprobar_dialog_revfin(self, show: bool):
        self.show_aprobar_dialog_revfin = show
        if not show:
            self.selected_solicitud_revfin = {}
    
    def set_show_rechazar_dialog_revfin(self, show: bool):
        self.show_rechazar_dialog_revfin = show
        if not show:
            self.selected_solicitud_revfin = {}
            self.motivo_rechazo_revfin = ""
    
    # Métodos de aprobación/rechazo para RevFin
    @rx.event
    def aprobar_solicitud_revfin(self):
        if not self.selected_solicitud_revfin:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return
        
        solicitud_id = self.selected_solicitud_revfin.get("id")
        revfin_usuario = self.current_revfin.get("usuario", "Revisor Financiero")
        
        result = FinanciamientoApi.aprobar_por_revfin(solicitud_id, revfin_usuario)
        
        if result:
            self.close_aprobar_dialog_revfin()
            
            self.loading_revfin = True
            yield
            yield self.load_data_revfin()
            self.loading_revfin = False
            
            yield rx.toast.success(f"✅ Solicitud aprobada por Revisor Financiero")
        else:
            yield rx.toast.error("❌ Error al aprobar la solicitud")
    
    @rx.event
    def rechazar_solicitud_revfin(self):
        if not self.selected_solicitud_revfin:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return
        
        solicitud_id = self.selected_solicitud_revfin.get("id")
        motivo = self.motivo_rechazo_revfin if self.motivo_rechazo_revfin else "Rechazado por Revisor Financiero"
        
        result = FinanciamientoApi.rechazar_solicitud_fin(solicitud_id, motivo)
        
        if result:
            self.close_rechazar_dialog_revfin()
            
            self.loading_revfin = True
            yield
            yield self.load_data_revfin()
            self.loading_revfin = False
            
            yield rx.toast.success("✅ Solicitud rechazada")
        else:
            yield rx.toast.error("❌ Error al rechazar la solicitud")
    
    # Cerrar sesión RevFin
    @rx.event
    def sign_out_revfin(self):
        self.is_authenticated_revfin = False
        self.current_revfin = {}
        
        yield rx.toast.success(
            "✅ Sesión cerrada exitosamente",
            position="top-right",
            duration=3000
        )
        
        yield rx.redirect(Route.REVFIN_LOGIN.value)
    
    # Variables computadas
    @rx.var
    def solicitudes_count_revfin(self) -> int:
        return len(self.solicitudes_pendientes_revfin)
    
    @rx.var
    def revfin_name(self) -> str:
        return self.current_revfin.get("usuario", "Revisor Financiero")