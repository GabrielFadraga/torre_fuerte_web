import reflex as rx
import TFuerte.utils as utils
from TFuerte.components.navbar import navbar
from TFuerte.components.navbar_about import navbar_about
from TFuerte.components.info_text import info_text
from TFuerte.views.header.header import header
from TFuerte.views.header.header_about import header_about
from TFuerte.views.header.header_projects import gallery
#from TFuerte.views.header.responsive_projects import gallery
from TFuerte.views.links.links import links
from TFuerte.components.footer import footer
from TFuerte.components.link_button import link_button
import TFuerte.styles.styles as styles
from TFuerte.views.sponsor.sponsor import sponsor
from rxconfig import config
from TFuerte.routes import Route
from TFuerte.components.sidebar import sidebar

from TFuerte.styles.colors import Text_tx 


@rx.page(
    route=Route.PROJECTS.value,
    title="Nuestros proyectos",
    description="Aquí evidenciamos los logros de Torre Fuerte",
    image="tff.png"
)
def projects() -> rx.Component:
    return rx.box(
        utils.lang(),

        navbar("Nuestros proyectos"),
        rx.center(
            rx.vstack(
                gallery(),

                align_items="center",
                max_width=styles.TEAM_WIDTH,
                margin=styles.Spacer.BIG.value,
                width="100%",
                spacing="2",
                padding=styles.Spacer.BIG.value,

            ),
        ),
        rx.vstack(
        footer(),
        width="100%",
        align_items="center",
            ),
        align_items="center",
        
        
)