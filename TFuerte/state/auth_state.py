import reflex as rx
from TFuerte.api.supabase_auth import SupabaseAuth
from TFuerte.routes import Route

class AuthState(rx.State):
    """Estado para manejar la autenticación"""
    
    # Variables de estado
    email: str = ""
    password: str = ""
    confirm_password: str = ""
    error_message: str = ""
    success_message: str = ""
    loading: bool = False
    is_authenticated: bool = False
    current_user: dict = {}
    
    async def on_load(self):
        """Verificar autenticación al cargar cualquier página"""
        print("🔄 Verificando autenticación en on_load...")
        
        # Obtener usuario desde Supabase (lee token de localStorage)
        user = SupabaseAuth.get_current_user()
        
        if user:
            self.is_authenticated = True
            self.current_user = {
                "id": user.id,
                "email": user.email,
                "created_at": str(user.created_at),
            }
            print(f"✅ Usuario autenticado: {self.current_user['email']}")
        else:
            self.is_authenticated = False
            self.current_user = {}
            print("❌ No hay usuario autenticado")
    
    def set_email(self, email: str):
        self.email = email
    
    def set_password(self, password: str):
        self.password = password
    
    def set_confirm_password(self, confirm_password: str):
        self.confirm_password = confirm_password
    
    def sign_up(self):
        """Registrar nuevo usuario"""
        self.loading = True
        self.error_message = ""
        self.success_message = ""
        yield
        
        if not self.email or not self.password:
            self.error_message = "Email y contraseña son requeridos"
            self.loading = False
            return
        
        if self.password != self.confirm_password:
            self.error_message = "Las contraseñas no coinciden"
            self.loading = False
            return
        
        response = SupabaseAuth.sign_up(self.email, self.password)
        
        if response["success"]:
            self.success_message = "Usuario registrado exitosamente. Verifica tu email."
            self.email = ""
            self.password = ""
            self.confirm_password = ""
            
            yield rx.toast.success(
                "Registro exitoso. Verifica tu email.",
                position="top-right",
                duration=5000
            )
            
            # Redirigir al login después de 2 segundos
            yield rx.call_script(f"setTimeout(() => window.location.href = '{Route.ADMIN_LOGIN.value}', 2000)")
        else:
            self.error_message = response["error"] or "Error al registrar usuario"
            
            yield rx.toast.error(
                self.error_message,
                position="top-right",
                duration=5000
            )
        
        self.loading = False
    
    def sign_in(self):
        """Iniciar sesión"""
        self.loading = True
        self.error_message = ""
        self.success_message = ""
        yield
        
        if not self.email or not self.password:
            self.error_message = "Email y contraseña son requeridos"
            self.loading = False
            return
        
        response = SupabaseAuth.sign_in(self.email, self.password)
        
        if response["success"]:
            self.is_authenticated = True
            self.current_user = {
                "id": response["user"].id,
                "email": response["user"].email,
                "created_at": str(response["user"].created_at),
            }
            self.email = ""
            self.password = ""
            
            yield rx.toast.success(
                "Inicio de sesión exitoso",
                position="top-right",
                duration=3000
            )
            
            # Redirigir al dashboard
            yield rx.redirect(Route.ADMIN1.value)
        else:
            self.error_message = response["error"] or "Error al iniciar sesión"
            
            yield rx.toast.error(
                self.error_message,
                position="top-right",
                duration=5000
            )
        
        self.loading = False
    
    def sign_out(self):
        """Cerrar sesión"""
        response = SupabaseAuth.sign_out()
        
        if response["success"]:
            self.is_authenticated = False
            self.current_user = {}
            self.email = ""
            self.password = ""
            
            yield rx.toast.success(
                "Sesión cerrada exitosamente",
                position="top-right",
                duration=3000
            )
            
            # Redirigir al login
            yield rx.redirect(Route.ADMIN_LOGIN.value)
        else:
            yield rx.toast.error(
                "Error al cerrar sesión",
                position="top-right",
                duration=3000
            )