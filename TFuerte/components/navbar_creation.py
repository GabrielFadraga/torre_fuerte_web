import reflex as rx
from TFuerte.styles.colors import Text_tx, Color_tx
from TFuerte.styles.fonts import FontWeight as FontWeight
from TFuerte.styles.fonts import Fonts_tx as Fonts_tx
from TFuerte.components.title import title as title
import TFuerte.styles.styles as styles
from TFuerte.routes import Route


def creation() -> rx.Component:
    return rx.desktop_only(
            rx.box(
            rx.hstack(
            rx.spacer(),
            rx.hstack(
                rx.link("Inicio", href=Route.INDEX.value, color="white", _hover={"color": "orange"}, size="8"),
                rx.link("Nosotros", href=Route.ABOUT.value, color="white", _hover={"color": "orange"}, size="8"),
                rx.link("Servicios", href=Route.SERVICES.value, color="white", _hover={"color": "orange"}, size="8"),
                rx.link("Cartera", href=Route.PROJECTS.value, color="white", _hover={"color": "orange"}, size="8"),
                rx.link("Grupo", href=Route.TEAM.value, color="white", _hover={"color": "orange"}, size="8"),
                rx.link("Contacto", href="#contacto", color="white", _hover={"color": "orange"}, size="8"),
                spacing="7",
                
                width="100%",
                align="end",
                justify="end",
            ),
        width="100%",
        
            
        ),
        width="100%"
        ),
        width="100%",
        style=styles.navbar_title_style,
        padding=styles.Spacer.DEFAULT.value,
        align="end",
        justify="end",
        top="0",
        z_index="1000",
        #padding="1.5em",
        background_color="#194264FF",
    )