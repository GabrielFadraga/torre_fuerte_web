import reflex as rx
import TFuerte.utils as utils
from TFuerte.components.navbar import navbar
from TFuerte.components.info_text import info_text
from TFuerte.views.header.header import header
from TFuerte.views.header.header_img import header_img
from TFuerte.views.links.links import links
from TFuerte.components.footer import footer
from TFuerte.components.link_button import link_button
import TFuerte.styles.styles as styles
from TFuerte.views.sponsor.sponsor import sponsor
from TFuerte.components.navbar_creation import creation
from TFuerte.views.header.header_creation import headcreat
from TFuerte.views.header.logo_header import logo
from rxconfig import config

from TFuerte.styles.colors import Text_tx 


@rx.page(
    title="Torre Fuerte",
    description="Con la mirada en lo alto",
    image="tff.png"
)
def index() -> rx.Component:
    return rx.box(
        rx.vstack(
        utils.lang(),
        creation(),
        headcreat(),
        logo(),
        #footer(),

                #align_items="center",
                max_width=styles.MAX_WIDTH,
                #margin=styles.Spacer.DEFAULT.value,
                #margin_y=styles.Spacer.DEFAULT.value,
                
                width="100%",
                spacing="4",
                

            ),
        rx.vstack(
        sponsor(),
        footer(),
        width="100%",
        #align_items="center",
            ),
        width="100%",
        
    )


