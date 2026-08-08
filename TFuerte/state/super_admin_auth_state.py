# TFuerte/state/super_admin_auth_state.py
import reflex as rx
from TFuerte.api.user_management_api import SuperAdminAPI
from TFuerte.routes import Route

class SuperAdminAuthState(rx.State):
    username: str = ""
    password: str = ""
    error_message: str = ""
    loading: bool = False
    is_authenticated: bool = False
    current_user: dict = {}

    def set_username(self, username: str):
        self.username = username

    def set_password(self, password: str):
        self.password = password

    def login(self):
        self.loading = True
        self.error_message = ""
        yield

        if not self.username or not self.password:
            self.error_message = "Usuario y contraseña son requeridos"
            self.loading = False
            return

        user = SuperAdminAPI.authenticate(self.username, self.password)
        if user:
            self.is_authenticated = True
            self.current_user = user
            self.username = ""
            self.password = ""
            yield rx.toast.success("Inicio de sesión exitoso", position="top-right")
            yield rx.redirect(Route.USER_MANAGEMENT.value)
        else:
            self.error_message = "Credenciales inválidas"
            yield rx.toast.error("Credenciales inválidas", position="top-right")

        self.loading = False

    def logout(self):
        self.is_authenticated = False
        self.current_user = {}
        yield rx.redirect(Route.SUPER_ADMIN_LOGIN.value)

    def check_auth(self):
        if not self.is_authenticated:
            return rx.redirect(Route.SUPER_ADMIN_LOGIN.value)
        return