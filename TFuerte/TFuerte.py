import reflex as rx
import TFuerte.styles.styles as styles
from TFuerte.pages.index import index
from TFuerte.pages.about import about
from TFuerte.pages.services import services
from TFuerte.pages.projects import projects
from TFuerte.pages.team import team
from TFuerte.pages.taller import taller
from TFuerte.pages.eventos import event
from TFuerte.pages.testing import testing
from TFuerte.pages.auth_login import auth
from TFuerte.pages.auth_signup import auth
#from TFuerte.views.admin.dashboard import admin_dashboard
from TFuerte.pages.dashboard1 import admin_dashboard
from TFuerte.pages.admin_login_new import admin_login_new
from TFuerte.pages.solicitante_login import solicitante_login
from TFuerte.pages.admin_dashboard import admin_dashboard
from TFuerte.pages.solicitante_dashboard import solicitante_dashboard
from TFuerte.pages.panels_admin import user_selection

from rxconfig import config


app = rx.App(
    stylesheets=styles.StyleSheets,
    style=styles.BASE_STYLES
)