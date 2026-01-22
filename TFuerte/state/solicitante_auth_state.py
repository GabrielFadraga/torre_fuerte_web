import reflex as rx
from TFuerte.api.solicitante_auth_api import SolicitanteAuthAPI
from TFuerte.routes import Route
from TFuerte.state.solicitante_dashboard_state import SolicitanteDashboardState

class SolicitanteAuthState(rx.State):
    """Estado para manejar autenticación de solicitantes"""
    
    # Variables de estado (Vars)
    usuario: str = ""
    clave: str = ""
    error_message: str = ""
    success_message: str = ""
    loading: bool = False
    is_authenticated: bool = False
    current_solicitante: dict = {}
    
    def set_usuario(self, usuario: str):
        self.usuario = usuario
    
    def set_clave(self, clave: str):
        self.clave = clave
    
    @rx.event
    def sign_in(self):
        """Iniciar sesión como solicitante"""
        self.loading = True
        self.error_message = ""
        self.success_message = ""
        yield
        
        # Aquí self.usuario y self.clave son strings normales, podemos usar if
        if not self.usuario or not self.clave:
            self.error_message = "Usuario y clave son requeridos"
            self.loading = False
            return
        
        response = SolicitanteAuthAPI.sign_in(self.usuario, self.clave)
        
        if response["success"]:
            self.is_authenticated = True
            self.current_solicitante = response["user"]
            
            print(f"✅ Solicitante autenticado: {self.current_solicitante}")
            print(f"📋 ID Personalizado (id_custom): {self.current_solicitante.get('id_custom')}")
            
            # Pasar la información del solicitante al estado del dashboard
            yield SolicitanteDashboardState.set_solicitante_info(self.current_solicitante)
            
            # Limpiar campos sensibles
            self.clave = ""
            
            yield rx.toast.success(
                "✅ Inicio de sesión exitoso",
                position="top-right",
                duration=3000
            )
            
            # Redirigir al dashboard
            yield rx.redirect(Route.SOLICITANTE_DASHBOARD.value)
        else:
            self.error_message = response["error"] or "Error al iniciar sesión"
            
            yield rx.toast.error(
                self.error_message,
                position="top-right",
                duration=5000
            )
        
        self.loading = False
    
    @rx.event
    def sign_out(self):
        """Cerrar sesión de solicitante"""
        self.is_authenticated = False
        self.current_solicitante = {}
        self.usuario = ""
        self.clave = ""
        
        yield rx.toast.success(
            "✅ Sesión cerrada exitosamente",
            position="top-right",
            duration=3000
        )
        
        yield rx.redirect(Route.SOLICITANTE_LOGIN.value)