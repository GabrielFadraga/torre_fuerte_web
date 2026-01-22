# TFuerte/state/admin_auth_state.py
import reflex as rx
from TFuerte.api.admin_auth_api import AdminAuthAPI
from TFuerte.routes import Route

class AdminAuthState(rx.State):
    """Estado para manejar autenticación de administradores"""
    
    # Variables de estado
    username: str = ""
    password: str = ""
    error_message: str = ""
    success_message: str = ""
    loading: bool = False
    is_authenticated: bool = False
    current_admin: dict = {}
    
    def set_username(self, username: str):
        self.username = username
    
    def set_password(self, password: str):
        self.password = password
    
    # TFuerte/state/admin_auth_state.py - MODIFICAR EL MÉTODO sign_in
    def sign_in(self):
        """Iniciar sesión como administrador"""
        self.loading = True
        self.error_message = ""
        self.success_message = ""
        yield
        
        if not self.username or not self.password:
            self.error_message = "Usuario y contraseña son requeridos"
            self.loading = False
            return
        
        response = AdminAuthAPI.sign_in(self.username, self.password)
        
        if response["success"]:
            self.is_authenticated = True
            self.current_admin = response["user"]
            
            # Almacenar el nombre de usuario en AdminDashboardState
            from TFuerte.state.admin_dashboard_state import AdminDashboardState
            AdminDashboardState.admin_username = self.username
            
            self.username = ""
            self.password = ""
            
            yield rx.toast.success(
                "✅ Inicio de sesión exitoso",
                position="top-right",
                duration=3000
            )
            
            # Redirigir al dashboard de administración
            yield rx.redirect(Route.ADMIN_DASHBOARD.value)
        else:
            self.error_message = response["error"] or "Error al iniciar sesión"
            
            yield rx.toast.error(
                self.error_message,
                position="top-right",
                duration=5000
            )
        
        self.loading = False
    
    def sign_out(self):
        """Cerrar sesión de administrador"""
        self.is_authenticated = False
        self.current_admin = {}
        self.username = ""
        self.password = ""
        
        yield rx.toast.success(
            "✅ Sesión cerrada exitosamente",
            position="top-right",
            duration=3000
        )
        
        # Redirigir al login de administradores
        yield rx.redirect(Route.ADMIN_LOGIN_NEW.value)