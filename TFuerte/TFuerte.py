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

from TFuerte.pages.solicitante_rm_form import solicitante_rm_form
from TFuerte.pages.tecnica_login import tecnica_login
from TFuerte.pages.tecnica_dashboard import tecnica_dashboard
from TFuerte.pages.admin_rm_login import admin_rm_login
from TFuerte.pages.admin_rm_dashboard import admin_rm_dashboard
from TFuerte.pages.logistica_login import logistica_login
from TFuerte.pages.logistica_dashboard import logistica_dashboard
from TFuerte.pages.solicitante_rm_login import solicitante_login

from TFuerte.pages.revfin_dashboard import revfin_dashboard
from TFuerte.pages.revfin_login import revfin_login

from TFuerte.pages.panels_admin import user_selection
from TFuerte.pages.admin_tf_login import admin_tf_login

from TFuerte.pages.generar_comprobante import generar_comprobante

from rxconfig import config


app = rx.App(
    stylesheets=styles.StyleSheets,
    style=styles.BASE_STYLES
)