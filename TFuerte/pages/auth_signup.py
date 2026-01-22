import reflex as rx
from TFuerte.routes import Route
import TFuerte.utils as utils
from TFuerte.components.navbar import navbar
from TFuerte.components.scroll_top import scroll_top_button
from TFuerte.components.footer import footer, footer_final
from TFuerte.views.header.header_auth_signup import auth_signup
import TFuerte.styles.styles as styles
from TFuerte.routes import Route
from TFuerte.styles.colors import Text_tx 
from rxconfig import config
from TFuerte.state.auth_state import AuthState

#@rx.page(
#    route=Route.ADMIN_SIGNUP.value,
#    title="Torre Fuerte Administración",
#    description="Acceso limitado",
#    image="tff.png",
#    on_load=AuthState.on_load  # Verificar autenticación
#)
def auth() -> rx.Component:
    return rx.box(
        utils.lang(),
        navbar("Estricto"),
        rx.vstack(
            auth_signup(),
            scroll_top_button(),
            align_items="center",
            max_width=styles.TEAM_WIDTH,
            margin_y=styles.Spacer.SMALL.value,
            width="100%",
            spacing="2",
        ),
        align_items="center",
        width="100%",
    )