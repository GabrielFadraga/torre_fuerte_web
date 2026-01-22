import reflex as rx
from enum import Enum

class Route(Enum):
    INDEX = "/"
    ABOUT = "/about"
    SERVICES = "/services"
    PROJECTS = "/projects"
    TEAM = "/team"
    TALLER = "/taller"
    EVENTOS = "/eventos"
    TESTING = "/db"
    ADMIN_LOGIN = "/authlogin"
    #ADMIN_SIGNUP = "/authsignup"
    ADMIN = "/dashboard"
    ADMIN1 = "/dashboard1"

    # Nuevas rutas para el sistema de permisos
    ADMIN_LOGIN_NEW = "/admin-login-new"  # Login para administradores (tabla Autorizacion)
    SOLICITANTE_LOGIN = "/solicitante-login"  # Login para solicitantes (tabla Solicitantes)
    ADMIN_DASHBOARD = "/admin-dashboard"  # Dashboard de administradores
    SOLICITANTE_DASHBOARD = "/solicitante-dashboard"  # Dashboard de solicitantes

    ADMIN_PAGE = "/admin_page"