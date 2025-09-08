import reflex as rx
import TFuerte.utils as utils
from TFuerte.components.navbar import navbar
from TFuerte.components.info_text import info_text
from TFuerte.views.header.header import header
from TFuerte.views.links.links import links
from TFuerte.components.footer import footer
from TFuerte.components.link_button import link_button
import TFuerte.styles.styles as styles
from TFuerte.views.sponsor.sponsor import sponsor
from rxconfig import config

from TFuerte.styles.colors import Text_tx 


@rx.page(
    title="Torre Fuerte",
    description="Con la mirada en lo alto",
    image="tff.png"
)
def index() -> rx.Component:
    return rx.box(
        utils.lang(),
        navbar("Bienvenidos a Torre Fuerte"),
        rx.center(
            rx.vstack(
                header(),
                links(),
                sponsor(),

                align_items="center",
                max_width=styles.MAX_WIDTH,
                margin_y=styles.Spacer.BIG.value,
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

