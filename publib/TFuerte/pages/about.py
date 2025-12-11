import reflex as rx
import TFuerte.utils as utils
from TFuerte.components.navbar import navbar
from TFuerte.views.header.header_about import about_with_animations
import TFuerte.styles.styles as styles
from rxconfig import config
from TFuerte.routes import Route
from TFuerte.components.sidebar import sidebar
from TFuerte.components.scroll_top import scroll_top_button
from TFuerte.components.footer import footer, footer_final

from TFuerte.styles.colors import Text_tx 


@rx.page(
    route=Route.ABOUT.value,
    title="Sobre nosotros",
    description="Sobre la empresa",
    image="tff.png"
)
def about() -> rx.Component:
    return rx.box(
        utils.lang(),

        navbar("Sobre nosotros"),
            rx.vstack(
            about_with_animations(),
            
            scroll_top_button(),
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