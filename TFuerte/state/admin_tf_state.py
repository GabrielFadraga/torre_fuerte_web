import reflex as rx
from TFuerte.api.admin_tf_api import AdminTFApi
from TFuerte.routes import Route

class AdminTFState(rx.State):
    """Estado para la autenticación del panel de administración de almacén"""
    
    # Credenciales para login
    username: str = ""
    password: str = ""
    error_message: str = ""
    loading: bool = False
    
    # Usuario actual
    current_admin: dict = {}
    is_authenticated: bool = False
    
    # Setters
    def set_username(self, username: str):
        self.username = username
    
    def set_password(self, password: str):
        self.password = password
    
    @rx.event
    def sign_in(self):
        """Inicia sesión como administrador del sistema"""
        self.loading = True
        self.error_message = ""
        yield
        
        if not self.username or not self.password:
            self.error_message = "Usuario y contraseña son requeridos"
            self.loading = False
            return
        
        response = AdminTFApi.sign_in(self.username, self.password)
        
        if response["success"]:
            user = response["user"]
            self.is_authenticated = True
            self.current_admin = user
            
            # Limpiar campos
            self.username = ""
            self.password = ""
            
            yield rx.toast.success(
                "✅ Inicio de sesión exitoso",
                position="top-right",
                duration=3000
            )
            
            # Redirigir a la página de selección de usuario
            yield rx.redirect(Route.ADMIN_PAGE.value)
        else:
            self.error_message = response["error"] or "Error al iniciar sesión"
            yield rx.toast.error(
                self.error_message,
                position="top-right",
                duration=4000
            )
        
        self.loading = False
    
    @rx.event
    def sign_out(self):
        """Cierra la sesión del administrador"""
        self.is_authenticated = False
        self.current_admin = {}
        
        yield rx.toast.success(
            "✅ Sesión cerrada exitosamente",
            position="top-right",
            duration=3000
        )
        
        yield rx.redirect(Route.ADMIN_LOGIN_PANEL.value)
    
    # Variables computadas
    @rx.var
    def admin_name(self) -> str:
        return self.current_admin.get("usuario", "Administrador")
    
    @rx.var
    def admin_id(self) -> int:
        return self.current_admin.get("id", 0)