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

    # Nuevas rutas para el sistema RM
    SOLICITANTE_RM_FORM = "/solicitante/rm-form"
    TECNICA_DASHBOARD = "/tecnica/dashboard"
    ADMIN_RM_DASHBOARD = "/admin/rm-dashboard"
    LOGISTICA_DASHBOARD = "/logistica/dashboard"
    TECNICA_LOGIN = "/tecnica/login"
    ADMIN_RM_LOGIN = "/admin-rm/login"
    LOGISTICA_LOGIN = "/logistica/login"

    SOLICITANTERM_LOGIN = "/solicitante_rm/login"
    
    REVFIN_DASHBOARD = "/revfin/dashboard"
    REVFIN_LOGIN = "/revfin/login"

    ADMIN_LOGIN_PANEL = "/admin-tf-login"

    GENERAR_COMPROBANTE = "/generar-comprobante"