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
from TFuerte.api.api import hello

from TFuerte.styles.colors import Text_tx 

class IndexState(rx.State):
    colors: list[str] = ["black", "red", "green", "blue", "purple"]

    index: int = 0

    @rx.event
    def next_color(self):
        """An event handler to go to the next color."""
        # Event handlers can modify the base vars.
        # Here we reference the base vars `colors` and `index`.
        self.index = (self.index + 1) % len(self.colors)

    @rx.var
    def color(self) -> str:
        """A computed var that returns the current color."""
        # Computed vars update automatically when the state changes.
        return self.colors[self.index]

    @rx.var()
    def sayhello(self) -> str:
        return hello()

@rx.page(
    title="Torre Fuerte",
    description="Con la mirada en lo alto",
    image="tff.png"
)
def index() -> rx.Component:
    return rx.box(
        utils.lang(),
        
        rx.text(IndexState.sayhello,
                on_click=IndexState.next_color,
                color=IndexState.color,
                _hover={"cursor": "pointer"},

            ),
        
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


