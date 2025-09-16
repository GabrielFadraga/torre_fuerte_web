import reflex as rx
from TFuerte.styles.colors import Text_tx, Color_tx
from rxconfig import config
from TFuerte.routes import Route
import TFuerte.styles.styles as styles
from TFuerte.components.navbar_creation import creation
from TFuerte.views.header.header_creation import headcreat
from TFuerte.views.header.logo_header import logo
from TFuerte.components.footer import footer
from TFuerte.views.sponsor.sponsor import sponsor

@rx.page(
    route=Route.CREATION.value,
    title="Torre Fuerte",
    description="Con la mirada en lo alto"
)

def my_creation() -> rx.Component:
    return rx.vstack(

        creation(),
        headcreat(),
        logo(),
        footer(),


        width="100%",
        spacing="4"
    )