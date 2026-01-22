import reflex as rx
from TFuerte.routes import Route
import TFuerte.utils as utils
from TFuerte.components.navbar import navbar
from TFuerte.components.scroll_top import scroll_top_button
from TFuerte.components.footer import footer, footer_final
from TFuerte.views.header.header_auth_login import auth_login 
from TFuerte.state.auth_state import AuthState
import TFuerte.styles.styles as styles
from TFuerte.routes import Route
from TFuerte.styles.colors import Text_tx 
from rxconfig import config

@rx.page(
    route=Route.ADMIN_LOGIN.value,
    title="Torre Fuerte Administración",
    description="Acceso limitado",
    image="tff.png",
    on_load=AuthState.on_load  # Verificar autenticación
)
def auth() -> rx.Component:
    return rx.box(
        utils.lang(),
        navbar("Estricto"),
        rx.vstack(
            # El componente auth_login() que ya tienes
            # Asegúrate de que use AuthState.sign_in en el botón
            auth_login(),
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