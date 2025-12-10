import reflex as rx
import TFuerte.utils as utils
from TFuerte.components.navbar import navbar
from TFuerte.components.sidebar import sidebar
from TFuerte.components.scroll_top import scroll_top_button
from TFuerte.components.info_text import info_text
from TFuerte.views.header.header import header
from TFuerte.views.header.header_img import header_img
from TFuerte.views.links.links import links
from TFuerte.components.footer import footer, footer_final
from TFuerte.components.link_button import link_button
import TFuerte.styles.styles as styles
from TFuerte.views.sponsor.sponsor import sponsor, sponsor_final
from TFuerte.components.navbar_creation import creation
from TFuerte.views.header.header_creation import headcreat, headcreat_final
from TFuerte.views.header.logo_header import logo
from TFuerte.views.header.logo_responsive import logo_resp
from rxconfig import config

from TFuerte.styles.colors import Text_tx 

class State(rx.State):
    """Define your app state here."""

@rx.page(
    title="Torre Fuerte",
    description="Con la mirada en lo alto",
    image="tff.png"
)
def index() -> rx.Component:
    return rx.box(
        utils.lang(),
        
        rx.vstack(
        creation(),

        headcreat_final(),

    
        spacing="5",
        width="100%",
    ),   
        rx.vstack(
        logo(),
        
        scroll_top_button(),
        align_items="center",        
        #margin=styles.Spacer.SMALL.value,
        margin_y=styles.Spacer.SMALL.value,

            
        width="100%",
        spacing="2",
        max_width=styles.TEAM_WIDTH,
                
                
    ),
        rx.vstack(
        sponsor_final(),
        footer_final(),
        width="100%",
        align="center",
            ),
        width="100%",
        
    )


