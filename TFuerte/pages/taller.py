import reflex as rx
import TFuerte.utils as utils
from TFuerte.components.navbar import navbar
from TFuerte.components.navbar_about import navbar_about
from TFuerte.components.info_text import info_text
from TFuerte.views.header.header import header
from TFuerte.views.header.header_taller import taller_creative_section
from TFuerte.views.header.header_about import about_with_animations
from TFuerte.views.header.header_abres import header_abres
from TFuerte.views.links.links import links
from TFuerte.components.footer import footer
from TFuerte.components.link_button import link_button
import TFuerte.styles.styles as styles
from TFuerte.views.sponsor.sponsor import sponsor
from TFuerte.rxconfig import config
from TFuerte.routes import Route
from TFuerte.components.sidebar import sidebar
from TFuerte.components.scroll_top import scroll_top_final
from TFuerte.components.footer import footer, footer_final

from TFuerte.styles.colors import Text_tx 


@rx.page(
    route=Route.TALLER.value,
    title="Nuestro Taller",
    description="Taller de Mecánica",
    image="tff.png"
)
def taller() -> rx.Component:
    return rx.box(
        utils.lang(),

        navbar("Taller"),
            rx.vstack(
            taller_creative_section(),
            
            scroll_top_final(),
            width="100%",
            spacing="5",
            ),
        rx.vstack(
        footer_final(),
        width="100%",
        align_items="center",
            ),
        align="start",
        width="100%",

)