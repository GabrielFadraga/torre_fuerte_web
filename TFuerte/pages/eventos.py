import reflex as rx
import TFuerte.utils as utils
from TFuerte.components.navbar import navbar
from TFuerte.components.scroll_top import scroll_top_button
from TFuerte.views.header.header import header
from TFuerte.views.header.header_img import header_img
from TFuerte.views.header.header_events import event1
from TFuerte.components.footer import footer, footer_final
import TFuerte.styles.styles as styles
from TFuerte.routes import Route

from rxconfig import config

from TFuerte.styles.colors import Text_tx 

@rx.page(
    route=Route.EVENTOS.value,
    title="Torre Fuerte",
    description="Con la mirada en lo alto",
    image="tff.png"
)
def event() -> rx.Component:
    return rx.box(
        utils.lang(),

        navbar("Eventos más importantes"),
            rx.vstack(
                event1(),

                scroll_top_button(),
                align_items="center",
                max_width=styles.TEAM_WIDTH,
                margin_y=styles.Spacer.SMALL.value,
                #margin=styles.Spacer.BIG.value,
                width="100%",
                spacing="2",
                #padding=styles.Spacer.BIG.value,

            ),
        rx.vstack(
        footer_final(),
        width="100%",
        align_items="center",
            ),
        align_items="center",
        spacing="9"
        
)