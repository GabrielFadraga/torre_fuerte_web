import reflex as rx
from TFuerte.styles.colors import Text_tx, Color_tx
from TFuerte.styles.fonts import FontWeight as FontWeight
from TFuerte.styles.fonts import Fonts_tx as Fonts_tx
from TFuerte.components.title import title as title
import TFuerte.styles.styles as styles
from TFuerte.routes import Route


def creation() -> rx.Component:
    return rx.hstack(
            rx.spacer(),
            rx.hstack(
                rx.link("Inicio", href=Route.CREATION.value, color="white", _hover={"color": "orange"}, size="8"),
                rx.link("Servicios", href=Route.SERVICES.value, color="white", _hover={"color": "orange"}, size="8"),
                rx.link("Nosotros", href=Route.ABOUT.value, color="white", _hover={"color": "orange"}, size="8"),
                rx.link("Contacto", href="#contacto", color="white", _hover={"color": "orange"}, size="8"),
                rx.link("Grupo", href=Route.TEAM.value, color="white", _hover={"color": "orange"}, size="8"),
                spacing="7",
                
            ),
            background_color="#194264FF",
            padding="1.5em",
            #position="sticky",
            top="0",
            z_index="1000",
            width="100%"
        )